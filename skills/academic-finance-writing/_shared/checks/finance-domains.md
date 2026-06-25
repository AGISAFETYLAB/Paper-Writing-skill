# Finance Domain Adapters

Use this reference after selecting the structural `paper_type`. Domain adapters adjust vocabulary,
variable families, literature map, institutional context, display pressure, and reviewer risks.
Domain adapters do not decide section order.

## Source Anchors

- American Economic Association JEL G: Financial Economics, including general financial markets,
  financial institutions and services, corporate finance and governance, behavioral finance, and
  household finance:
  https://www.aeaweb.org/econlit/jelCodes.php?view=jel
- American Economic Association JEL C guide: mathematical and quantitative methods are separated
  from applications, so method family must be recorded separately from the finance application:
  https://www.aeaweb.org/jel/guide/jel.php?class=C
- Elsevier financial-economics journal scopes list asset pricing, banking, corporate finance,
  behavioral finance, derivatives, entrepreneurial finance, fintech, international finance,
  market microstructure, real estate, risk management, and venture capital:
  https://shop.elsevier.com/subjects/journals/social-sciences-and-humanities/economics-and-finance/financial-economics
- Elsevier general financial-economics scope lists asset pricing, corporate finance, banking,
  international finance, risk management, derivatives, market microstructure, real estate finance,
  digital finance/fintech, behavioral finance, and sustainable/climate-related finance:
  https://shop.elsevier.com/journals/subjects/social-sciences-and-humanities/economics-and-finance/financial-economics/financial-economics-general
- Federal Reserve finance fields include asset pricing, banking and financial institutions,
  consumer finance, corporate finance, financial markets, market microstructure, portfolio choice,
  real estate, and risk management:
  https://www.federalreserve.gov/econres/market-microstructure-f.htm
- OECD digital finance describes digitally enabled financial innovation, payments, loans,
  investor/consumer protection, financial stability, and market integrity:
  https://www.oecd.org/en/topics/sub-issues/digital-finance.html
- Journal of Accounting Research states that accounting research includes finance, economics,
  statistics, psychology, sociology, disclosure, capital markets, governance, auditing, taxation,
  and related information and measurement questions:
  https://www.chicagobooth.edu/research/chookaszian/journal-of-accounting-research

## Domain Boundary

Choose one primary domain adapter and record secondary adapters only when they change terminology,
variables, literatures, displays, or reviewer risks. Do not let a domain adapter override the
selected structural paper-type profile. If the project is only "asset pricing", "corporate
finance", "banking", "fintech", or another finance field, first choose the structural profile
such as empirical research, theoretical model, short insight / letter, review/survey/perspective,
comment/replication/corrigendum, data/method/software, or generic finance paper.

Use the domain adapter to decide:

- which economic objects and institutional facts must be defined early,
- which variable families and sample filters require disclosure,
- which benchmark literatures and JEL codes are plausible starting points,
- which tables and figures reviewers will expect,
- which threats are domain-specific rather than generic econometric threats.

Do not use the domain adapter to decide:

- section order,
- whether the paper is empirical, theoretical, review, short letter, replication, or software/data,
- page window or target length,
- venue template or document format,
- whether a claim is causal, predictive, descriptive, or theoretical.

## Domain Adapter Table

| Domain adapter | Source basis | Writing use | Typical display pressure | Reviewer-risk emphasis |
|---|---|---|---|---|
| asset pricing and investments | JEL G1; Elsevier and Fed finance fields list asset pricing, portfolio choice, investments, financial markets, derivatives, and market efficiency | define returns, signals, portfolio formation, factors, benchmark models, rebalancing, investment universe, and economic magnitude | summary returns, portfolio-sort table, factor-model alpha table, cumulative performance, drawdown, turnover, liquidity/capacity checks | timing, look-ahead bias, data snooping, transaction costs, short-sale constraints, factor benchmark choice |
| corporate finance and governance | JEL G3; Elsevier and JFE scope list corporate finance, governance, capital structure, payout, M&A, contracting, investment, and risk management | define firm decisions, governance mechanisms, financing constraints, investment/payout outcomes, and agency or contracting channel | firm summary table, panel regression table, event-study table/plot, mechanism table, heterogeneity by governance or financing friction | endogeneity, omitted firm shocks, selection, reverse causality, institutional timing, external validity |
| banking and financial institutions | JEL G2; Elsevier and Fed fields list banking, financial institutions, intermediation, credit markets, regulation, solvency, and systemic risk | define institution type, balance-sheet variables, loan/credit exposures, regulation, capital, liquidity, risk, and supervisory setting | bank/loan panel table, credit/risk outcome table, policy-shock design figure, capital/liquidity diagnostics, systemic-risk display | regulatory confounding, risk controls, selection into treatment, balance-sheet measurement, institutional setting |
| market microstructure | JEL G1/G14/G18; Elsevier and Fed fields list market microstructure, trading, liquidity, market efficiency, high-frequency trading, and financial-market regulation | define market venue, trading clock, order/trade data, liquidity measures, price discovery, information events, and market design | intraday/event-time plot, liquidity/spread table, order-flow or volume panel, market-quality robustness grid | timing precision, market closures, multiple events, microstructure noise, venue-rule changes, clustered dependence |
| behavioral finance | JEL G4; Elsevier scope lists behavioral and experimental finance; Fed fields include consumer finance and portfolio choice | define beliefs, attention, sentiment, bias, decision frame, experimental task, or investor psychology channel | survey/experiment balance table, treatment-effect table, belief or attention distribution, sentiment/event response plot | construct validity, multiple hypotheses, external validity, mechanism versus anomaly, subject/sample selection |
| household finance | JEL G5; Fed fields include consumer finance; Elsevier scope lists personal finance and portfolio choice | define household unit, account/product type, saving/borrowing/wealth decision, literacy, advice, insurance, and consumer protection setting | household balance table, product choice table, treatment/event plot, distribution or binscatter, heterogeneity by wealth/literacy | representativeness, attrition, disclosure/privacy constraints, selection, measurement of wealth/debt/information |
| fintech and digital assets | Elsevier scope lists fintech, digital finance, blockchain, financial innovation, and alternative data; OECD digital finance covers payments, loans, innovation, stability, investor/consumer protection, and market integrity | define platform, protocol, payment/loan/token product, network, algorithmic decision, regulation, and market-integrity context | platform/network table, transaction-flow chart, adoption plot, token/market panel, regulation-event display | data access, survivorship, wash trading or manipulation, changing rules, investor protection, external validity |
| accounting and disclosure | AEA M accounting category plus JAR and accounting-finance scopes; finance scopes include capital markets, governance, disclosure, information users, and financial reporting | define disclosure event, filing type, accounting measure, information environment, audit/governance link, and market response | filing/sample table, disclosure measure validation, textual measure diagnostics, market-reaction plot, governance mechanism table | measure validity, disclosure endogeneity, restatement or filing-timing issues, omitted information events, textual construct drift |
| risk, insurance, and derivatives | JEL G13/G22/G32; Elsevier scope lists derivatives, hedging, risk management, actuarial studies, systemic risk, and term-structure models | define risk factor, contract, hedge, insurer/intermediary, exposure, pricing model, tail event, and risk-management objective | risk exposure table, option/derivative pricing panel, VaR/tail plot, hedge effectiveness table, stress-test display | model assumptions, tail dependence, calibration, liquidity, counterparty or margin rules, omitted risk exposures |
| macro, international, and monetary finance | JEL F3/G15 plus Elsevier scopes on international finance, exchange rates, capital flows, global cost of capital, and financial stability | define country/market system, exchange-rate or capital-flow measure, monetary shock, international channel, and policy regime | country-time summary table, exchange-rate/capital-flow plot, policy event study, macro-finance panel table | aggregation, concurrent macro shocks, country comparability, policy endogeneity, exchange-rate regime changes |
| ESG, climate, and sustainable finance | Elsevier general financial-economics scope lists sustainable and climate-related finance; finance scopes include energy finance, risk, regulation, and institutional investors | define ESG/climate exposure, rating or disclosure measure, transition/physical risk, policy event, green instrument, and investor channel | exposure validation table, rating disagreement plot, event/policy response, portfolio or cost-of-capital table | measurement disagreement, greenwashing, omitted policy/news shocks, causal overreach, materiality and horizon mismatch |
| real estate finance | JEL G21 and R real estate categories; Elsevier and Fed fields list real estate finance, mortgages, financial institutions, and financial markets | define property, mortgage/loan, REIT, collateral, local market, borrower, and valuation or credit channel | property/loan summary, geographic exposure map, mortgage performance table, local-market trend plot | local-market confounding, appraisal/valuation measurement, borrower selection, collateral and lender controls |
| private equity, venture capital, and entrepreneurial finance | JEL G24; Elsevier scope lists investment banking, venture capital, entrepreneurial finance, private markets, and financial contracting | define deal stage, fund, startup/private firm, investment terms, exit, governance rights, valuation, and selection process | deal/fund summary table, funding/exit event plot, valuation table, selection or survivorship diagnostics | selection, survivorship, stale valuation, treatment timing, proprietary-data coverage, external validity |

## Application Checklist

For each manuscript framework, record:

- `finance_domain_adapter`: one primary adapter from the table.
- `secondary_domain_adapters`: optional, only when needed.
- `domain_source_basis`: JEL G/JEL-adjacent category, publisher scope, Fed field, or policy source.
- `domain_changes_to_framework`: terminology, variables, displays, literature, and risks only.
- `paper_type_profile`: unchanged structural source of section order.

If the chosen domain is not covered, use `generic finance paper` as the structural paper type and
write a short custom domain note with source URL, date checked, terminology, display pressure, and
reviewer-risk differences.
