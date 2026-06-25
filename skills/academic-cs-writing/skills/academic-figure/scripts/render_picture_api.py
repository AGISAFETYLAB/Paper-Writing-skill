#!/usr/bin/env python3
"""Render a Picture Brief through a configured image API.

This script is intentionally small and provider-light. It reads the exact
``Direct Image Prompt`` block from a Picture Brief, calls the selected renderer,
and writes the returned image bytes to disk. It does not invent prompt content.
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_GEMINI_MODEL = "gemini-2.5-flash-image"
DEFAULT_OPENAI_MODEL = "gpt-image-2"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_section(markdown: str, heading: str) -> str:
    pattern = re.compile(rf"^##\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(markdown)
    if not match:
        raise ValueError(f"missing section: ## {heading}")
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    content = markdown[start:end].strip()
    if not content:
        raise ValueError(f"empty section: ## {heading}")
    return content


def extract_output_path(markdown: str) -> str | None:
    match = re.search(r"^- Output path:\s*(.+?)\s*$", markdown, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return None if not value or value.upper() == "TBD" else value


def extract_pdf_output_path(markdown: str) -> str | None:
    match = re.search(r"^- PDF output path:\s*(.+?)\s*$", markdown, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    return None if not value or value.upper() == "TBD" else value


def extract_allowed_labels(markdown: str) -> list[str]:
    match = re.search(r"^- Labels allowed in the image:\s*$", markdown, re.MULTILINE)
    if not match:
        return []
    start = match.end()
    next_heading = re.search(r"^##\s+", markdown[start:], re.MULTILINE)
    end = start + next_heading.start() if next_heading else len(markdown)
    labels: list[str] = []
    for line in markdown[start:end].splitlines():
        stripped = line.strip()
        if stripped.startswith("- ") and stripped[2:].endswith(":"):
            if labels:
                break
            continue
        bullet = re.match(r"^-\s+(.+?)\s*$", line)
        if bullet:
            value = bullet.group(1).strip()
            if value and value.upper() != "TBD":
                labels.append(value)
    return labels


def resolve_prompt(args: argparse.Namespace) -> tuple[str, str | None, str | None, list[str]]:
    if args.prompt:
        return args.prompt.strip(), None, None, []
    if args.prompt_file:
        return read_text(Path(args.prompt_file)).strip(), None, None, []
    if not args.brief:
        raise ValueError("provide --brief, --prompt-file, or --prompt")
    brief_path = Path(args.brief)
    markdown = read_text(brief_path)
    return (
        extract_section(markdown, "Direct Image Prompt"),
        extract_output_path(markdown),
        extract_pdf_output_path(markdown),
        extract_allowed_labels(markdown),
    )


def resolve_output(args: argparse.Namespace, brief_output: str | None) -> Path:
    if args.out:
        return Path(args.out).expanduser()
    if brief_output:
        return (Path.cwd() / brief_output).resolve() if not Path(brief_output).is_absolute() else Path(brief_output)
    raise ValueError("provide --out or include '- Output path:' in the Picture Brief")


def resolve_pdf_output(args: argparse.Namespace, brief_pdf_output: str | None, output_path: Path) -> Path | None:
    if args.no_pdf:
        return None
    if args.pdf_out:
        return Path(args.pdf_out).expanduser()
    if args.out:
        return output_path.with_suffix(".pdf")
    if brief_pdf_output:
        path = Path(brief_pdf_output)
        return (Path.cwd() / path).resolve() if not path.is_absolute() else path
    return output_path.with_suffix(".pdf")


def request_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=body, headers=headers, method="POST")
    if os.environ.get("IMAGE_API_NO_PROXY", "").strip() in {"1", "true", "TRUE", "yes", "YES"}:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        open_request = opener.open
    else:
        open_request = urllib.request.urlopen
    try:
        with open_request(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        error_text = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from image API: {error_text[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"image API request failed: {exc}") from exc
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"image API returned non-JSON response: {raw[:200]!r}") from exc


def walk_json(value: Any) -> list[Any]:
    found = [value]
    if isinstance(value, dict):
        for child in value.values():
            found.extend(walk_json(child))
    elif isinstance(value, list):
        for child in value:
            found.extend(walk_json(child))
    return found


def decode_image_from_response(response: dict[str, Any]) -> bytes:
    # Gemini-style: {"inlineData": {"mimeType": "image/png", "data": "..."}}
    for item in walk_json(response):
        if isinstance(item, dict):
            inline = item.get("inlineData") or item.get("inline_data")
            if isinstance(inline, dict) and inline.get("data"):
                return base64.b64decode(str(inline["data"]))
            if item.get("b64_json"):
                return base64.b64decode(str(item["b64_json"]))
    # Some relays return OpenAI-style data entries.
    data = response.get("data")
    if isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and item.get("b64_json"):
                return base64.b64decode(str(item["b64_json"]))
    raise RuntimeError("image API response did not contain inline image data")


def parse_aspect_ratio(value: str) -> float:
    text = value.strip().lower().replace("x", ":")
    if ":" in text:
        left, right = text.split(":", 1)
        width = float(left)
        height = float(right)
    else:
        width = float(text)
        height = 1.0
    if width <= 0 or height <= 0:
        raise ValueError("aspect ratio must be positive")
    return width / height


def load_font(size: int) -> Any:
    from PIL import ImageFont

    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size=size)
    return ImageFont.load_default()


def overlay_horizontal_bottom_labels(
    canvas: Any,
    labels: list[str],
    *,
    band_top: float = 0.66,
    label_y: float = 0.82,
    font_size: int | None = None,
) -> Any:
    from PIL import ImageDraw

    if not labels:
        return canvas
    draw = ImageDraw.Draw(canvas)
    width, height = canvas.size
    top = max(0, min(height, int(round(height * band_top))))
    y = max(0, min(height, int(round(height * label_y))))
    draw.rectangle((0, top, width, height), fill=(255, 255, 255))
    size = font_size or max(18, min(42, int(round(height * 0.11))))
    font = load_font(size)
    for idx, label in enumerate(labels):
        x = width * (idx + 0.5) / len(labels)
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        draw.text(
            (x - text_width / 2, y - text_height / 2),
            label,
            fill=(17, 24, 39),
            font=font,
        )
    return canvas


def postprocess_image_bytes(
    image: bytes,
    *,
    trim_whitespace: bool = False,
    trim_threshold: int = 10,
    trim_pad: int = 32,
    pad_aspect: str | None = None,
    overlay_labels: list[str] | None = None,
    overlay_layout: str = "none",
    overlay_band_top: float = 0.66,
    overlay_y: float = 0.82,
    overlay_font_size: int | None = None,
) -> bytes:
    if not trim_whitespace and not pad_aspect and overlay_layout == "none":
        return image
    try:
        from PIL import Image, ImageChops
    except ImportError as exc:
        raise RuntimeError("Pillow is required for image postprocessing") from exc

    with Image.open(io.BytesIO(image)) as opened:
        canvas = opened.convert("RGB")

    if trim_whitespace:
        background = Image.new("RGB", canvas.size, canvas.getpixel((0, 0)))
        diff = ImageChops.difference(canvas, background).convert("L")
        mask = diff.point(lambda value: 255 if value > trim_threshold else 0)
        bbox = mask.getbbox()
        if bbox:
            left, top, right, bottom = bbox
            left = max(0, left - trim_pad)
            top = max(0, top - trim_pad)
            right = min(canvas.width, right + trim_pad)
            bottom = min(canvas.height, bottom + trim_pad)
            canvas = canvas.crop((left, top, right, bottom))

    if pad_aspect:
        target_ratio = parse_aspect_ratio(pad_aspect)
        current_ratio = canvas.width / canvas.height
        if current_ratio < target_ratio:
            new_width = int(round(canvas.height * target_ratio))
            new_height = canvas.height
        else:
            new_width = canvas.width
            new_height = int(round(canvas.width / target_ratio))
        if new_width != canvas.width or new_height != canvas.height:
            padded = Image.new("RGB", (new_width, new_height), (255, 255, 255))
            x = (new_width - canvas.width) // 2
            y = (new_height - canvas.height) // 2
            padded.paste(canvas, (x, y))
            canvas = padded

    if overlay_layout != "none":
        if overlay_layout != "horizontal-bottom":
            raise ValueError("unsupported --overlay-layout; expected none or horizontal-bottom")
        canvas = overlay_horizontal_bottom_labels(
            canvas,
            overlay_labels or [],
            band_top=overlay_band_top,
            label_y=overlay_y,
            font_size=overlay_font_size,
        )

    out = io.BytesIO()
    canvas.save(out, format="PNG")
    return out.getvalue()


def call_gemini(prompt: str, timeout: int) -> tuple[bytes, str]:
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is not set")
    base_url = os.environ.get("GEMINI_BASE_URL", "https://generativelanguage.googleapis.com").strip().rstrip("/")
    model = os.environ.get("GEMINI_IMAGE_MODEL", DEFAULT_GEMINI_MODEL).strip() or DEFAULT_GEMINI_MODEL
    url = f"{base_url}/v1beta/models/{model}:generateContent"
    payload = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"responseModalities": ["IMAGE", "TEXT"]},
    }
    headers = {"Content-Type": "application/json", "x-goog-api-key": api_key}
    response = request_json(url, headers, payload, timeout)
    return decode_image_from_response(response), f"Gemini-compatible API ({model})"


def call_openai(prompt: str, timeout: int) -> tuple[bytes, str]:
    api_key = os.environ.get("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com").strip().rstrip("/")
    model = os.environ.get("OPENAI_IMAGE_MODEL", DEFAULT_OPENAI_MODEL).strip() or DEFAULT_OPENAI_MODEL
    url = f"{base_url}/v1/images/generations"
    payload = {"model": model, "prompt": prompt, "n": 1, "size": "1024x1024"}
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    response = request_json(url, headers, payload, timeout)
    return decode_image_from_response(response), f"OpenAI-compatible image API ({model})"


def choose_renderer(requested: str) -> str:
    if requested != "auto":
        return requested
    if os.environ.get("GEMINI_API_KEY", "").strip():
        return "gemini"
    if os.environ.get("OPENAI_API_KEY", "").strip():
        return "openai"
    raise RuntimeError("no image renderer configured; set GEMINI_API_KEY or OPENAI_API_KEY")


def write_image(path: Path, image: bytes) -> None:
    if len(image) < 64:
        raise RuntimeError("decoded image is unexpectedly small")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(image)


def write_pdf(path: Path, image: bytes) -> None:
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError("Pillow is required to write the PDF copy") from exc
    with Image.open(io.BytesIO(image)) as opened:
        if opened.mode in {"RGBA", "LA"}:
            background = Image.new("RGB", opened.size, (255, 255, 255))
            background.paste(opened, mask=opened.getchannel("A"))
            canvas = background
        else:
            canvas = opened.convert("RGB")
        path.parent.mkdir(parents=True, exist_ok=True)
        canvas.save(path, "PDF", resolution=300.0)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render a Picture Brief through Gemini/OpenAI image API.")
    parser.add_argument("--brief", help="Picture Brief Markdown file containing ## Direct Image Prompt")
    parser.add_argument("--prompt-file", help="Plain text file containing the exact image prompt")
    parser.add_argument("--prompt", help="Exact image prompt string")
    parser.add_argument("--out", help="Output image path. Defaults to '- Output path:' in the brief.")
    parser.add_argument("--pdf-out", help="Output PDF wrapper path. Defaults to a sibling .pdf next to --out.")
    parser.add_argument("--no-pdf", action="store_true", help="Do not write the paper-friendly PDF wrapper copy.")
    parser.add_argument("--renderer", choices=["auto", "gemini", "openai"], default="auto")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--trim-whitespace", action="store_true", help="Crop white/near-white empty margins before writing the image.")
    parser.add_argument("--trim-threshold", type=int, default=10, help="Pixel difference threshold for --trim-whitespace.")
    parser.add_argument("--trim-pad", type=int, default=32, help="Padding in pixels kept around the trimmed content.")
    parser.add_argument("--pad-aspect", help="Pad the image to a target aspect ratio such as 3:1 or 16:9.")
    parser.add_argument("--overlay-labels-from-brief", action="store_true", help="Overlay exact labels parsed from the Picture Brief.")
    parser.add_argument("--overlay-labels", help="Comma-separated labels to overlay after rendering.")
    parser.add_argument("--overlay-layout", choices=["none", "horizontal-bottom"], default="none")
    parser.add_argument("--overlay-band-top", type=float, default=0.66, help="Top of the white label band as a fraction of image height.")
    parser.add_argument("--overlay-y", type=float, default=0.82, help="Vertical center for overlaid labels as a fraction of image height.")
    parser.add_argument("--overlay-font-size", type=int, help="Font size for overlaid labels.")
    parser.add_argument("--dry-run", action="store_true", help="Print selected renderer and prompt length; do not call API.")
    args = parser.parse_args(argv)

    try:
        prompt, brief_output, brief_pdf_output, brief_labels = resolve_prompt(args)
        output_path = resolve_output(args, brief_output)
        pdf_output_path = resolve_pdf_output(args, brief_pdf_output, output_path)
        renderer = choose_renderer(args.renderer)
        overlay_labels = [label.strip() for label in (args.overlay_labels or "").split(",") if label.strip()]
        if args.overlay_labels_from_brief:
            overlay_labels = brief_labels
        if args.dry_run:
            print(json.dumps({
                "renderer": renderer,
                "output": str(output_path),
                "pdf_output": str(pdf_output_path) if pdf_output_path else None,
                "prompt_chars": len(prompt),
                "overlay_labels": overlay_labels,
            }, indent=2))
            return 0
        if renderer == "gemini":
            image, route = call_gemini(prompt, args.timeout)
        elif renderer == "openai":
            image, route = call_openai(prompt, args.timeout)
        else:
            raise RuntimeError(f"unsupported renderer: {renderer}")
        image = postprocess_image_bytes(
            image,
            trim_whitespace=args.trim_whitespace,
            trim_threshold=args.trim_threshold,
            trim_pad=args.trim_pad,
            pad_aspect=args.pad_aspect,
            overlay_labels=overlay_labels,
            overlay_layout=args.overlay_layout,
            overlay_band_top=args.overlay_band_top,
            overlay_y=args.overlay_y,
            overlay_font_size=args.overlay_font_size,
        )
        write_image(output_path, image)
        if pdf_output_path:
            write_pdf(pdf_output_path, image)
        print(json.dumps({
            "renderer": route,
            "output": str(output_path),
            "pdf_output": str(pdf_output_path) if pdf_output_path else None,
            "bytes": len(image),
            "postprocess": {
                "trim_whitespace": bool(args.trim_whitespace),
                "pad_aspect": args.pad_aspect,
                "overlay_layout": args.overlay_layout,
                "overlay_labels": overlay_labels,
            },
        }, indent=2))
        return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
