#!/usr/bin/env python3
"""Minimal paper-figure MCP display helper.

This server is deliberately narrow: it classifies display ideas, writes simple
FigureSpec JSON skeletons, renders deterministic SVG schematics, and writes
Picture Brief prompts under a caller-provided workspace. It does not create
paper claims, results, citations, prose, or image-generation API calls.
"""

from __future__ import annotations

import json
import os
import sys
import textwrap
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


sys.stdout = os.fdopen(sys.stdout.fileno(), "wb", buffering=0)
sys.stdin = os.fdopen(sys.stdin.fileno(), "rb", buffering=0)

SERVER_NAME = "paper-figure"
PROTOCOL_VERSION = "2024-11-05"
_use_ndjson = False


def send_response(response: dict[str, Any]) -> None:
    global _use_ndjson
    payload = json.dumps(response, ensure_ascii=True, separators=(",", ":")).encode("utf-8")
    if _use_ndjson:
        sys.stdout.write(payload + b"\n")
    else:
        header = f"Content-Length: {len(payload)}\r\n\r\n".encode("utf-8")
        sys.stdout.write(header + payload)
    sys.stdout.flush()


def read_message() -> dict[str, Any] | None:
    global _use_ndjson
    line = sys.stdin.readline()
    if not line:
        return None
    text = line.decode("utf-8").rstrip("\r\n")
    if text.lower().startswith("content-length:"):
        try:
            length = int(text.split(":", 1)[1].strip())
        except ValueError:
            return None
        while True:
            header_line = sys.stdin.readline()
            if not header_line:
                return None
            if header_line in {b"\r\n", b"\n"}:
                break
        body = sys.stdin.read(length)
        try:
            return json.loads(body.decode("utf-8"))
        except json.JSONDecodeError:
            return None
    if text.startswith("{"):
        _use_ndjson = True
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
    return None


def tool_result(request_id: Any, text: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": {"content": [{"type": "text", "text": text}]},
    }


def tool_error(request_id: Any, message: str) -> dict[str, Any]:
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": -32000, "message": message},
    }


def classify_figure(args: dict[str, Any]) -> dict[str, Any]:
    figure_id = str(args.get("figure_id", "<figure-id>"))
    figure_type = str(args.get("type_hint", "")).lower()
    message = str(args.get("message", "")).lower()
    source = str(args.get("source", "")).lower()

    route = "picture"
    workflow = "picture"
    section = args.get("section") or "TBD"
    output = f"paper/figures/{figure_id}.png"

    plot_terms = ["result", "metric", "accuracy", "rate", "curve", "ablation", "scaling", "csv", "json"]
    diagram_terms = ["architecture", "pipeline", "workflow", "system", "component", "taxonomy", "overview"]
    picture_terms = ["teaser", "illustration", "picture", "concept", "visual summary"]
    table_terms = ["table", "comparison", "baseline", "benchmark statistics"]

    haystack = " ".join([figure_type, message, source])
    if any(term in haystack for term in table_terms):
        route = "LaTeX table"
        workflow = "table"
        output = "paper/figures/tables/<figure-id>.tex"
    elif any(term in haystack for term in plot_terms) or source.endswith((".csv", ".json", ".tsv")):
        route = "reproducible plot script"
        workflow = "plot"
        output = f"paper/figures/{figure_id}.pdf"
    elif any(term in haystack for term in diagram_terms):
        route = "deterministic schematic (FigureSpec/SVG)"
        workflow = "schematic"
        output = "JSON spec + SVG/PDF under paper/figures/"
    elif any(term in haystack for term in picture_terms):
        route = "Picture Brief + optional picture renderer"
        workflow = "picture"
        output = f"Picture Brief + paper/figures/{figure_id}.png"
    elif "screenshot" in haystack or "example" in haystack or "qualitative" in haystack:
        route = "existing asset"
        workflow = "picture"
        output = "copied asset under paper/figures/"

    return {
        "route": route,
        "workflow": workflow,
        "section": section,
        "recommended_output": output,
        "caption_policy": "State the figure message, the comparison or mechanism, and the supported claim.",
    }


def safe_output_path(cwd: str, relpath: str) -> Path:
    root = Path(cwd).expanduser().resolve()
    path = (root / relpath).resolve()
    if root != path and root not in path.parents:
        raise ValueError("output path must stay under cwd")
    return path


def as_int(value: Any, fallback: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return fallback


def template_node(
    node_id: str,
    label: str,
    x: int,
    y: int,
    *,
    width: int = 150,
    height: int = 58,
    fill: str = "#F2F6FA",
    stroke: str = "#446C8E",
    text_color: str = "#18232E",
    highlight: bool = False,
    shape: str = "rounded",
    subtitle: str = "",
) -> dict[str, Any]:
    node = {
        "id": node_id,
        "label": label,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "shape": shape,
        "fill": fill,
        "stroke": stroke,
        "text_color": text_color,
    }
    if highlight:
        node["highlight"] = True
    if subtitle:
        node["subtitle"] = subtitle
    return node


def template_group(label: str, x: int, y: int, width: int, height: int, fill: str, stroke: str) -> dict[str, Any]:
    return {
        "label": label,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "fill": fill,
        "stroke": stroke,
    }


def build_figurespec_template(template: str, figure_id: str, title: str) -> dict[str, Any]:
    """Return a reusable, visually balanced FigureSpec template."""
    template = template.lower().replace("_", "-")
    if template in {"framework", "method", "overview"}:
        template = "pipeline"
    if template in {"benchmark-construction", "dataset"}:
        template = "benchmark"
    if template not in {"minimal", "pipeline", "architecture", "taxonomy", "benchmark"}:
        raise ValueError(
            "unknown template; expected one of: minimal, pipeline, architecture, taxonomy, benchmark"
        )

    if template == "minimal":
        return {
            "canvas": {"width": 720, "height": 320},
            "title": title,
            "nodes": [
                template_node("input", "Input", 70, 145),
                template_node("method", "Method", 285, 145, highlight=True, fill="#EAF3F8", stroke="#2E6F95"),
                template_node("evidence", "Evidence", 500, 145, fill="#F5F0E6", stroke="#9A6A2F"),
            ],
            "edges": [
                {"from": "input", "to": "method", "label": "feeds"},
                {"from": "method", "to": "evidence", "label": "supports"},
            ],
            "groups": [],
            "metadata": {"figure_id": figure_id, "template": template},
        }

    if template == "pipeline":
        return {
            "canvas": {"width": 1080, "height": 260},
            "title": title,
            "nodes": [
                template_node("input", "Input Data", 60, 120, fill="#EAF6F0", stroke="#4D9078"),
                template_node("task", "Task Setup", 245, 120, fill="#EEF3FA", stroke="#4C6F9F"),
                template_node(
                    "novel_module",
                    "Novel Module",
                    430,
                    110,
                    width=170,
                    height=78,
                    fill="#EAF3F8",
                    stroke="#216C96",
                    highlight=True,
                    subtitle="paper contribution",
                ),
                template_node("quality", "Quality Gate", 640, 120, fill="#F7F0E5", stroke="#A06A2D"),
                template_node("evaluation", "Evaluation", 825, 120, fill="#F0EEF8", stroke="#725AA8"),
            ],
            "edges": [
                {"from": "input", "to": "task", "label": "prepare"},
                {"from": "task", "to": "novel_module", "label": "solve"},
                {"from": "novel_module", "to": "quality", "label": "filter"},
                {"from": "quality", "to": "evaluation", "label": "measure"},
            ],
            "groups": [
                template_group("Problem Context", 35, 45, 365, 160, "#F8FBF9", "#C7DCD3"),
                template_group("Proposed Pipeline", 415, 35, 405, 180, "#F9FBFD", "#C6D8E5"),
                template_group("Evidence Link", 835, 45, 195, 160, "#FAF8FD", "#D8CFEB"),
            ],
            "metadata": {"figure_id": figure_id, "template": template},
        }

    if template == "architecture":
        return {
            "canvas": {"width": 1040, "height": 460},
            "title": title,
            "nodes": [
                template_node("user_input", "User / Data", 80, 70, fill="#EAF6F0", stroke="#4D9078"),
                template_node("interface", "Interface", 310, 70, fill="#EEF3FA", stroke="#4C6F9F"),
                template_node("controller", "Controller", 540, 70, fill="#EEF3FA", stroke="#4C6F9F"),
                template_node("core", "Core Method", 405, 205, width=190, height=78, fill="#EAF3F8", stroke="#216C96", highlight=True),
                template_node("memory", "Resources", 160, 325, fill="#F7F0E5", stroke="#A06A2D"),
                template_node("tools", "Tools / Models", 405, 325, fill="#F7F0E5", stroke="#A06A2D"),
                template_node("output", "Output", 735, 205, fill="#F0EEF8", stroke="#725AA8"),
            ],
            "edges": [
                {"from": "user_input", "to": "interface", "label": "request"},
                {"from": "interface", "to": "controller", "label": "dispatch"},
                {"from": "controller", "to": "core", "label": "orchestrate"},
                {"from": "memory", "to": "core", "label": "retrieve"},
                {"from": "tools", "to": "core", "label": "execute"},
                {"from": "core", "to": "output", "label": "produce"},
            ],
            "groups": [
                template_group("Input Layer", 45, 40, 675, 110, "#F8FAFC", "#CBD5E1"),
                template_group("Method Layer", 360, 180, 435, 130, "#F8FBFD", "#C6D8E5"),
                template_group("Support Layer", 115, 300, 510, 105, "#FCFAF5", "#E2D1AF"),
            ],
            "metadata": {"figure_id": figure_id, "template": template},
        }

    if template == "taxonomy":
        return {
            "canvas": {"width": 980, "height": 430},
            "title": title,
            "nodes": [
                template_node("root", "Task Taxonomy", 395, 70, width=190, fill="#EAF3F8", stroke="#216C96", highlight=True),
                template_node("axis_a", "Axis A", 90, 210, fill="#EAF6F0", stroke="#4D9078"),
                template_node("axis_b", "Axis B", 305, 210, fill="#EEF3FA", stroke="#4C6F9F"),
                template_node("axis_c", "Axis C", 520, 210, fill="#F7F0E5", stroke="#A06A2D"),
                template_node("axis_d", "Axis D", 735, 210, fill="#F0EEF8", stroke="#725AA8"),
                template_node("examples", "Examples / Cases", 395, 335, width=190, fill="#F8F8F8", stroke="#6B7280"),
            ],
            "edges": [
                {"from": "root", "to": "axis_a", "label": "category"},
                {"from": "root", "to": "axis_b", "label": "category"},
                {"from": "root", "to": "axis_c", "label": "category"},
                {"from": "root", "to": "axis_d", "label": "category"},
                {"from": "axis_b", "to": "examples", "label": "instantiates"},
                {"from": "axis_c", "to": "examples", "label": "instantiates"},
            ],
            "groups": [
                template_group("Definition Space", 55, 175, 870, 125, "#FAFBFC", "#D5DCE4"),
                template_group("Grounding", 345, 315, 290, 80, "#F8FBF9", "#C7DCD3"),
            ],
            "metadata": {"figure_id": figure_id, "template": template},
        }

    return {
        "canvas": {"width": 1080, "height": 270},
        "title": title,
        "nodes": [
            template_node("sources", "Raw Sources", 55, 125, fill="#EAF6F0", stroke="#4D9078"),
            template_node("criteria", "Inclusion Criteria", 240, 125, fill="#EEF3FA", stroke="#4C6F9F"),
            template_node("annotation", "Annotation", 450, 115, width=170, height=78, fill="#EAF3F8", stroke="#216C96", highlight=True),
            template_node("audit", "Audit / Agreement", 670, 125, fill="#F7F0E5", stroke="#A06A2D"),
            template_node("benchmark", "Benchmark Split", 860, 125, fill="#F0EEF8", stroke="#725AA8"),
        ],
        "edges": [
            {"from": "sources", "to": "criteria", "label": "filter"},
            {"from": "criteria", "to": "annotation", "label": "label"},
            {"from": "annotation", "to": "audit", "label": "verify"},
            {"from": "audit", "to": "benchmark", "label": "release"},
        ],
        "groups": [
            template_group("Collection", 30, 45, 390, 170, "#F8FBF9", "#C7DCD3"),
            template_group("Construction", 435, 35, 415, 200, "#F9FBFD", "#C6D8E5"),
            template_group("Dataset Output", 865, 45, 170, 170, "#FAF8FD", "#D8CFEB"),
        ],
        "metadata": {"figure_id": figure_id, "template": template},
    }


def infer_template(args: dict[str, Any]) -> str:
    explicit = str(args.get("template", "")).strip().lower()
    if explicit:
        return explicit
    haystack = " ".join(
        str(args.get(key, "")) for key in ("figure_id", "title", "figure_type", "message")
    ).lower()
    if "taxonomy" in haystack:
        return "taxonomy"
    if "benchmark" in haystack or "dataset" in haystack:
        return "benchmark"
    if "architecture" in haystack or "system" in haystack:
        return "architecture"
    return "pipeline"


def validate_figurespec(spec: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    canvas = spec.get("canvas", {})
    width = as_int(canvas.get("width"), 0)
    height = as_int(canvas.get("height"), 0)
    if width <= 0 or height <= 0:
        raise ValueError("FigureSpec canvas.width and canvas.height must be positive")

    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("FigureSpec must contain a non-empty nodes list")
    if not isinstance(edges, list):
        raise ValueError("FigureSpec edges must be a list")
    if not isinstance(groups, list):
        raise ValueError("FigureSpec groups must be a list")

    seen: set[str] = set()
    for node in nodes:
        node_id = str(node.get("id", "")).strip()
        if not node_id:
            raise ValueError("every node needs a non-empty id")
        if node_id in seen:
            raise ValueError(f"duplicate node id: {node_id}")
        seen.add(node_id)
        x = float(node.get("x", 0))
        y = float(node.get("y", 0))
        node_width = float(node.get("width", 120))
        node_height = float(node.get("height", 48))
        if node_width <= 0 or node_height <= 0:
            raise ValueError(f"node {node_id} must have positive width and height")
        if x < 0 or y < 0 or x + node_width > width or y + node_height > height:
            raise ValueError(f"node {node_id} crosses the canvas boundary")
        label = str(node.get("label", node_id))
        if max((len(part) for part in label.splitlines()), default=0) > 34:
            warnings.append(f"node {node_id} has a long label; prefer a short label and expand in the caption")

    for edge in edges:
        src = str(edge.get("from", "")).strip()
        tgt = str(edge.get("to", "")).strip()
        if src not in seen or tgt not in seen:
            raise ValueError(f"edge references unknown node: {src}->{tgt}")

    for group in groups:
        label = str(group.get("label", "group"))
        x = float(group.get("x", 0))
        y = float(group.get("y", 0))
        group_width = float(group.get("width", 0))
        group_height = float(group.get("height", 0))
        if group_width <= 0 or group_height <= 0:
            raise ValueError(f"group {label} must have positive width and height")
        if x < 0 or y < 0 or x + group_width > width or y + group_height > height:
            raise ValueError(f"group {label} crosses the canvas boundary")

    return warnings


def write_figurespec_skeleton(args: dict[str, Any]) -> dict[str, Any]:
    cwd = str(args.get("cwd", "."))
    figure_id = str(args.get("figure_id", "fig_overview"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/specs/{figure_id}.json"))
    title = str(args.get("title", ""))
    if args.get("nodes") is not None or args.get("edges") is not None:
        spec = {
            "canvas": args.get("canvas") or {"width": 900, "height": 420},
            "title": title,
            "nodes": args.get("nodes") or [],
            "edges": args.get("edges") or [],
            "groups": args.get("groups", []),
            "metadata": {
                "figure_id": figure_id,
                "template": "custom",
                "note": "Generated custom skeleton. Verify semantic accuracy before rendering.",
            },
        }
    else:
        template = infer_template(args)
        spec = build_figurespec_template(template, figure_id, title)
        spec.setdefault("metadata", {})["note"] = (
            "Generated from a built-in schematic template. Replace placeholder labels with exact paper terms."
        )

    warnings = validate_figurespec(spec)
    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return {"path": str(output_path), "spec": spec, "warnings": warnings}


def wrap_label(label: str, max_chars: int) -> list[str]:
    lines: list[str] = []
    for raw_line in str(label).splitlines() or [""]:
        wrapped = textwrap.wrap(raw_line, width=max_chars, break_long_words=False, break_on_hyphens=False)
        lines.extend(wrapped or [""])
    return lines[:4]


def add_multiline_text(
    parent: ET.Element,
    x: float,
    y: float,
    lines: list[str],
    *,
    font_size: int = 12,
    fill: str = "#18232E",
    weight: str = "500",
    css_class: str = "",
) -> None:
    if not lines:
        return
    line_height = font_size + 3
    start_y = y - (line_height * (len(lines) - 1)) / 2
    attrs = {
        "x": f"{x:.1f}",
        "y": f"{start_y:.1f}",
        "text-anchor": "middle",
        "font-size": str(font_size),
        "font-weight": weight,
        "fill": fill,
    }
    if css_class:
        attrs["class"] = css_class
    text_el = ET.SubElement(parent, "text", attrs)
    for idx, line in enumerate(lines):
        tspan_attrs = {"x": f"{x:.1f}"}
        if idx:
            tspan_attrs["dy"] = str(line_height)
        tspan = ET.SubElement(text_el, "tspan", tspan_attrs)
        tspan.text = line


def node_box(node: dict[str, Any]) -> tuple[float, float, float, float]:
    return (
        float(node.get("x", 0)),
        float(node.get("y", 0)),
        float(node.get("width", 120)),
        float(node.get("height", 48)),
    )


def connection_point(src: tuple[float, float, float, float], tgt: tuple[float, float, float, float]) -> tuple[float, float, float, float]:
    sx, sy, sw, sh = src
    tx, ty, tw, th = tgt
    scx = sx + sw / 2
    scy = sy + sh / 2
    tcx = tx + tw / 2
    tcy = ty + th / 2
    dx = tcx - scx
    dy = tcy - scy
    if abs(dx) >= abs(dy):
        if dx >= 0:
            return sx + sw, scy, tx, tcy
        return sx, scy, tx + tw, tcy
    if dy >= 0:
        return scx, sy + sh, tcx, ty
    return scx, sy, tcx, ty + th


def draw_edge(svg: ET.Element, x1: float, y1: float, x2: float, y2: float, label: str) -> None:
    if abs(y1 - y2) < 1 or abs(x1 - x2) < 1:
        path_data = f"M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"
    else:
        mid_x = (x1 + x2) / 2
        path_data = f"M{x1:.1f},{y1:.1f} C{mid_x:.1f},{y1:.1f} {mid_x:.1f},{y2:.1f} {x2:.1f},{y2:.1f}"
    ET.SubElement(svg, "path", {"class": "edge-line", "d": path_data})
    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 8
        ET.SubElement(svg, "text", {"class": "edge-text", "x": f"{mx:.1f}", "y": f"{my:.1f}"}).text = label


def render_figurespec(args: dict[str, Any]) -> dict[str, Any]:
    """Render a FigureSpec JSON file or inline spec to SVG.

    Reads nodes (with x, y, label, shape) and edges (from, to, label) and
    produces a clean academic-style SVG suitable for paper inclusion.
    """
    cwd = str(args.get("cwd", "."))
    spec_path = args.get("spec_path")
    spec_inline = args.get("spec")
    figure_id = str(args.get("figure_id", "fig_diagram"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/{figure_id}.svg"))

    # Load spec
    if spec_path is not None:
        spec_path_resolved = safe_output_path(cwd, str(spec_path))
        spec = json.loads(spec_path_resolved.read_text(encoding="utf-8"))
    elif spec_inline is not None:
        spec = spec_inline
    else:
        raise ValueError("render_figurespec requires spec_path or spec")

    warnings = validate_figurespec(spec)
    canvas = spec.get("canvas", {"width": 700, "height": 320})
    width = int(canvas.get("width", 700))
    height = int(canvas.get("height", 320))
    title = str(spec.get("title", figure_id))
    nodes = spec.get("nodes", [])
    edges = spec.get("edges", [])
    groups = spec.get("groups", [])

    # SVG namespace
    NS = "http://www.w3.org/2000/svg"
    ET.register_namespace("", NS)
    svg = ET.Element(
        "svg",
        {
            "xmlns": NS,
            "viewBox": f"0 0 {width} {height}",
            "width": str(width),
            "height": str(height),
            "font-family": "Arial, Helvetica, DejaVu Sans, sans-serif",
            "font-size": "11",
        },
    )

    # Style
    style = ET.SubElement(svg, "style")
    style.text = """
    .node-rect { stroke-width: 1.6; rx: 7; ry: 7; }
    .node-rect-highlight { stroke-width: 2.3; rx: 8; ry: 8; }
    .node-subtitle { fill: #5B6470; font-size: 9px; text-anchor: middle; }
    .edge-line { stroke: #4B5563; stroke-width: 1.35; fill: none; marker-end: url(#arrowhead); }
    .edge-text { fill: #4B5563; font-size: 9px; font-weight: 600; text-anchor: middle; }
    .group-rect { stroke-width: 1; stroke-dasharray: 4 4; rx: 8; ry: 8; }
    .group-label { fill: #667085; font-size: 10px; font-style: italic; font-weight: 600; }
    .figure-title { fill: #1F2937; font-size: 14px; font-weight: 700; text-anchor: middle; }
    .bg { fill: #ffffff; }
    """

    # Defs for arrowhead marker
    defs = ET.SubElement(svg, "defs")
    marker = ET.SubElement(
        defs,
        "marker",
        {
            "id": "arrowhead",
            "markerWidth": "8",
            "markerHeight": "6",
            "refX": "8",
            "refY": "3",
            "orient": "auto",
        },
    )
    ET.SubElement(marker, "path", {"d": "M0,0 L8,3 L0,6 Z", "fill": "#666666"})

    # Background
    ET.SubElement(svg, "rect", {"class": "bg", "x": "0", "y": "0", "width": str(width), "height": str(height)})

    # Groups (background regions)
    for group in groups:
        gx = int(group.get("x", 0))
        gy = int(group.get("y", 0))
        gw = int(group.get("width", 100))
        gh = int(group.get("height", 100))
        glabel = str(group.get("label", ""))
        gfill = str(group.get("fill", "#F8F8F8"))
        gstroke = str(group.get("stroke", "#CCCCCC"))
        ET.SubElement(
            svg,
            "rect",
            {
                "class": "group-rect",
                "x": str(gx),
                "y": str(gy),
                "width": str(gw),
                "height": str(gh),
                "fill": gfill,
                "stroke": gstroke,
            },
        )
        if glabel:
            label = ET.SubElement(
                svg,
                "text",
                {"class": "group-label", "x": str(gx + 6), "y": str(gy + 14)},
            )
            label.text = glabel

    # Edges (drawn before nodes so nodes sit on top)
    node_positions: dict[str, tuple[float, float, float, float]] = {}
    for node in nodes:
        nid = str(node.get("id", ""))
        node_positions[nid] = node_box(node)

    for edge in edges:
        src_id = str(edge.get("from", ""))
        tgt_id = str(edge.get("to", ""))
        elabel = str(edge.get("label", ""))

        if src_id in node_positions and tgt_id in node_positions:
            x1, y1, x2, y2 = connection_point(node_positions[src_id], node_positions[tgt_id])
            draw_edge(svg, x1, y1, x2, y2, elabel)

    # Nodes
    for node in nodes:
        nid = str(node.get("id", ""))
        nlabel = str(node.get("label", nid))
        nx = float(node.get("x", 0))
        ny = float(node.get("y", 0))
        nw = float(node.get("width", 120))
        nh = float(node.get("height", 48))
        nshape = str(node.get("shape", "rounded"))
        nhighlight = bool(node.get("highlight", False))
        fill = str(node.get("fill", "#F2F6FA"))
        stroke = str(node.get("stroke", "#446C8E"))
        text_color = str(node.get("text_color", "#18232E"))
        subtitle = str(node.get("subtitle", "")).strip()

        rect_class = "node-rect-highlight" if nhighlight else "node-rect"
        if nshape == "rounded":
            ET.SubElement(
                svg,
                "rect",
                {
                    "class": rect_class,
                    "x": str(nx),
                    "y": str(ny),
                    "width": str(nw),
                    "height": str(nh),
                    "rx": "8" if nhighlight else "7",
                    "ry": "8" if nhighlight else "7",
                    "fill": fill,
                    "stroke": stroke,
                },
            )
        elif nshape == "diamond":
            points = [
                (nx + nw / 2, ny),
                (nx + nw, ny + nh / 2),
                (nx + nw / 2, ny + nh),
                (nx, ny + nh / 2),
            ]
            ET.SubElement(
                svg,
                "polygon",
                {
                    "class": rect_class,
                    "points": " ".join(f"{px:.1f},{py:.1f}" for px, py in points),
                    "fill": fill,
                    "stroke": stroke,
                },
            )
        else:
            ET.SubElement(
                svg,
                "rect",
                {
                    "class": rect_class,
                    "x": str(nx),
                    "y": str(ny),
                    "width": str(nw),
                    "height": str(nh),
                    "rx": "0",
                    "ry": "0",
                    "fill": fill,
                    "stroke": stroke,
                },
            )

        center_x = nx + nw / 2
        center_y = ny + nh / 2 - (7 if subtitle else 0)
        max_chars = max(10, int(nw / 8.5))
        add_multiline_text(
            svg,
            center_x,
            center_y,
            wrap_label(nlabel, max_chars),
            font_size=12,
            fill=text_color,
            weight="700" if nhighlight else "600",
        )
        if subtitle:
            ET.SubElement(
                svg,
                "text",
                {"class": "node-subtitle", "x": f"{center_x:.1f}", "y": f"{ny + nh - 12:.1f}"},
            ).text = subtitle

    # Title at top
    if title:
        ET.SubElement(svg, "text", {"class": "figure-title", "x": str(width / 2), "y": "24"})
        svg[-1].text = title

    # Serialize
    svg_bytes = ET.tostring(svg, encoding="unicode", xml_declaration=False)
    # Pretty-print: add XML declaration and ensure newline
    svg_output = '<?xml version="1.0" encoding="UTF-8"?>\n' + svg_bytes + "\n"

    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg_output, encoding="utf-8")

    return {
        "path": str(output_path),
        "width": width,
        "height": height,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "group_count": len(groups),
        "warnings": warnings,
    }


def normalize_lines(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    if not text:
        return []
    return [line.strip() for line in text.splitlines() if line.strip()]


def markdown_bullets(items: list[str], fallback: str = "TBD") -> str:
    if not items:
        return f"- {fallback}"
    return "\n".join(f"- {item}" for item in items)


def configured_picture_renderer() -> tuple[str, str]:
    """Auto-detect picture API from standard environment variables.

    Priority: Gemini if GEMINI_API_KEY is set, else GPT-image if OPENAI_API_KEY
    is set, else current-agent drawing. This helper records the route only; it
    does not call image-generation APIs.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    openai_key = os.environ.get("OPENAI_API_KEY", "").strip()
    configured_status = "detected from standard provider environment; render in a separate picture-renderer step"

    if gemini_key:
        model = os.environ.get("GEMINI_IMAGE_MODEL", "").strip() or "gemini-2.5-flash-image"
        base_url = os.environ.get("GEMINI_BASE_URL", "").strip()
        route = f"Gemini-compatible API ({model})"
        if base_url:
            route = f"{route} via {base_url}"
        return route, configured_status

    if openai_key:
        model = os.environ.get("OPENAI_IMAGE_MODEL", "").strip() or "gpt-image-2"
        base_url = os.environ.get("OPENAI_BASE_URL", "").strip()
        route = f"GPT-image-compatible API ({model})"
        if base_url:
            route = f"{route} via {base_url}"
        return route, configured_status

    return "current executing agent", "no picture API configured; render step should use the current agent fallback"


def write_picture_brief(args: dict[str, Any]) -> dict[str, Any]:
    cwd = str(args.get("cwd", "."))
    figure_id = str(args.get("figure_id", "fig_picture"))
    output_relpath = str(args.get("output_relpath", f"paper/figures/prompts/{figure_id}.md"))
    title = str(args.get("title", figure_id))
    section = str(args.get("section", "TBD"))
    figure_type = str(args.get("figure_type", "picture illustration"))
    message = str(args.get("message", "TBD"))
    supported_claim = str(args.get("supported_claim", "TBD"))
    configured_renderer, renderer_status = configured_picture_renderer()
    renderer = str(args.get("renderer") or configured_renderer)
    renderer_status = str(args.get("renderer_status") or renderer_status)
    output_image = str(args.get("output_image", f"paper/figures/{figure_id}.png"))
    output_pdf = str(args.get("output_pdf", str(Path(output_image).with_suffix(".pdf"))))

    source_files = normalize_lines(args.get("source_files"))
    confirmed_concepts = normalize_lines(args.get("confirmed_concepts"))
    allowed_labels = normalize_lines(args.get("allowed_labels"))
    forbidden_labels = normalize_lines(args.get("forbidden_labels"))
    visual_elements = normalize_lines(args.get("visual_elements"))
    relationships = normalize_lines(args.get("relationships"))
    style = str(args.get("style", "clean white background, restrained academic palette, readable English labels"))
    avoid = normalize_lines(args.get("avoid")) or [
        "unsupported numbers",
        "invented modules",
        "decorative clip art",
        "rainbow gradients",
        "tiny unreadable text",
    ]

    elements_text = "; ".join(visual_elements) if visual_elements else "the confirmed visual elements"
    labels_text = ", ".join(f'"{label}"' for label in allowed_labels) if allowed_labels else "only labels confirmed by the paper plan"
    relationships_text = "; ".join(relationships) if relationships else "the confirmed relationships among the visual elements"
    avoid_text = "; ".join(avoid)
    direct_image_prompt = (
        "Create a publication-quality academic figure for a research paper. "
        f"The figure should communicate this message: {message}. "
        f"Show {elements_text}. "
        f"Render only these exact label strings, copied verbatim with identical spelling and capitalization: {labels_text}. "
        "Use clean, legible, correctly spelled sans-serif text; keep labels horizontal, short, and large enough to read at paper scale. "
        "Do not render spelling variants, aliases, example words, rubric headers, or extra captions; if uncertain, omit a label rather than misspell it. "
        f"Represent the relationships as {relationships_text}. "
        "Visual style requirements: flat vector illustration, clean lines, academic aesthetic, similar in restraint and clarity to figures in DeepMind or OpenAI papers. "
        "Use an organized flow suited to the content: left-to-right, top-to-bottom, circular, or another clear structure; group related components logically. "
        "Use professional pastel tones on a white background; fill the full frame and avoid large empty top or bottom bands. "
        "Text rendering is required: include legible text labels for the key modules or equations named in the methodology, such as Encoder, Loss, or Transformer only when those exact words are in the allowed label list. "
        f"Use this figure-specific style guidance: {style}. "
        f"Negative constraints: no photorealistic photos, no messy sketches, no unreadable text, no 3D shading artifacts, and avoid {avoid_text}. "
        "Do not add claims, modules, datasets, numbers, or labels that are not listed above."
    )

    brief = f"""# Picture Brief: {figure_id}

## Figure Identity
- Figure ID: {figure_id}
- Title: {title}
- Section: {section}
- Figure type: {figure_type}
- One-sentence message: {message}
- Supported claim: {supported_claim}

## Evidence Boundary
- Source files:
{markdown_bullets(source_files)}
- Confirmed concepts:
{markdown_bullets(confirmed_concepts)}
- Labels allowed in the image:
{markdown_bullets(allowed_labels)}
- Labels or claims forbidden in the image:
{markdown_bullets(forbidden_labels)}

## Visual Plan
- Canvas: publication figure, single-column or double-column as selected by the Paper Framework
- Layout: use the section and figure message above; avoid clutter and ambiguous flow
- Main visual elements:
{markdown_bullets(visual_elements)}
- Data flow or relationships:
{markdown_bullets(relationships)}
- Style: {style}
- Accessibility: readable at paper scale, colorblind-safe, grayscale-friendly

## Direct Image Prompt
{direct_image_prompt}

## Label Verification Plan
- Exact labels that must appear, spelled correctly:
{markdown_bullets(allowed_labels)}
- After rendering, confirm each visible word reads correctly and matches the paper terminology.
- If any label is garbled, duplicated, unsupported, or misspelled, regenerate or use the overlay fallback.

## Overlay Fallback Plan (only if the model misspells a label)
- Labels to overlay instead:
{markdown_bullets(allowed_labels)}
- Approximate normalized positions: TBD after inspecting the rendered image.

## Renderer Route
- Preferred renderer: {renderer}
- Renderer status: {renderer_status}
- Output path: {output_image}
- PDF output path: {output_pdf}
- API prompt source: use the exact `Direct Image Prompt` block above
- Review notes: inspect generated image for invented content, wrong labels, unreadable text, and wrong arrow direction before accepting it.
"""

    output_path = safe_output_path(cwd, output_relpath)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(brief, encoding="utf-8")
    return {
        "path": str(output_path),
        "output_image": output_image,
        "output_pdf": output_pdf,
        "direct_image_prompt": direct_image_prompt,
        "renderer": renderer,
        "renderer_status": renderer_status,
    }


def handle_request(request: dict[str, Any]) -> dict[str, Any] | None:
    method = request.get("method", "")
    params = request.get("params", {})
    request_id = request.get("id")

    if request_id is None:
        return None

    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": PROTOCOL_VERSION,
                "capabilities": {"tools": {}},
                "serverInfo": {"name": SERVER_NAME, "version": "0.2.0"},
            },
        }
    if method == "ping":
        return {"jsonrpc": "2.0", "id": request_id, "result": {}}
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "tools": [
                    {
                        "name": "classify_figure",
                        "description": "Classify a paper display idea into a plot, schematic, picture, or table route.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "figure_id": {"type": "string"},
                                "type_hint": {"type": "string"},
                                "section": {"type": "string"},
                                "message": {"type": "string"},
                                "source": {"type": "string"},
                            },
                        },
                    },
                    {
                        "name": "write_figurespec_skeleton",
                        "description": "Write a FigureSpec JSON skeleton under cwd using a built-in schematic template or caller-provided nodes and edges.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd", "figure_id"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "output_relpath": {"type": "string"},
                                "title": {"type": "string"},
                                "template": {
                                    "type": "string",
                                    "description": "Optional built-in template: pipeline, architecture, taxonomy, benchmark, or minimal.",
                                },
                                "message": {"type": "string"},
                                "canvas": {"type": "object"},
                                "nodes": {"type": "array"},
                                "edges": {"type": "array"},
                                "groups": {"type": "array"},
                            },
                        },
                    },
                    {
                        "name": "write_picture_brief",
                        "description": "Write a Markdown Picture Brief for a picture-style paper illustration under cwd. This does not call image APIs.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd", "figure_id"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "output_relpath": {"type": "string"},
                                "title": {"type": "string"},
                                "section": {"type": "string"},
                                "figure_type": {"type": "string"},
                                "message": {"type": "string"},
                                "supported_claim": {"type": "string"},
                                "renderer": {"type": "string"},
                                "output_image": {"type": "string"},
                                "output_pdf": {"type": "string"},
                                "source_files": {"type": "array"},
                                "confirmed_concepts": {"type": "array"},
                                "allowed_labels": {"type": "array"},
                                "forbidden_labels": {"type": "array"},
                                "visual_elements": {"type": "array"},
                                "relationships": {"type": "array"},
                                "style": {"type": "string"},
                                "avoid": {"type": "array"},
                            },
                        },
                    },
                    {
                        "name": "render_figurespec",
                        "description": "Validate and render a FigureSpec JSON (from write_figurespec_skeleton or hand-written) to an editable SVG diagram. Best for medium-complexity paper schematics; dense or unusual diagrams should move to hand-authored SVG/TikZ after the skeleton.",
                        "inputSchema": {
                            "type": "object",
                            "required": ["cwd"],
                            "properties": {
                                "cwd": {"type": "string"},
                                "figure_id": {"type": "string"},
                                "spec_path": {"type": "string", "description": "Path to a FigureSpec JSON file to render"},
                                "spec": {"type": "object", "description": "Inline FigureSpec object (alternative to spec_path)"},
                                "output_relpath": {"type": "string", "description": "Output SVG path relative to cwd"},
                            },
                        },
                    },
                ]
            },
        }
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        try:
            if name == "classify_figure":
                return tool_result(request_id, json.dumps(classify_figure(args), indent=2, ensure_ascii=False))
            if name == "write_figurespec_skeleton":
                return tool_result(request_id, json.dumps(write_figurespec_skeleton(args), indent=2, ensure_ascii=False))
            if name == "write_picture_brief":
                return tool_result(request_id, json.dumps(write_picture_brief(args), indent=2, ensure_ascii=False))
            if name == "render_figurespec":
                return tool_result(request_id, json.dumps(render_figurespec(args), indent=2, ensure_ascii=False))
            return tool_error(request_id, f"unknown tool: {name}")
        except Exception as exc:
            return tool_error(request_id, str(exc))
    return tool_error(request_id, f"unsupported method: {method}")


def main() -> None:
    while True:
        request = read_message()
        if request is None:
            break
        response = handle_request(request)
        if response is not None:
            send_response(response)


if __name__ == "__main__":
    main()
