# M-Tools repository instructions

Read the architecture and tool specification documents before making design or implementation decisions.

## Standing owner decision: Professional Marketing Workbench

M-Tools is a professional marketing manager's workbench and external memory, for practical use in the owner's future workplace and as everyday handy tools for marketing managers. Delegate recall of definitions, formulas, frameworks, procedural details and appropriate analysis to the tool; preserve conceptual understanding, strategic thinking, creativity, interpretation and human judgment.

- **Daily Utility first:** each tool must deliver standalone practical value. Never require a full pipeline or unrelated profile fields for a simple task.
- **Scientific Depth first:** eight reliable, scientifically grounded tools are more valuable than 29 superficial ones. Prioritize appropriate methods, evidence, validation and honest limitations over feature count.
- **Minimize Cognitive Load:** reuse relevant data, ask only for missing prerequisites, choose or suggest appropriate methods, and show understandable results, rationale and limitations. Keep formulas, assumptions, evidence and method details inspectable without requiring memorization. Never conceal uncertainty or replace human judgment.
- Every capability must address a real managerial task and define how practical utility, scientific validity and comprehensibility will be assessed. Do not expand solely to cover more concepts.

Canonical policy: [system architecture, section 0](docs/marketing-system-architecture-v1.md). Apply it to all design, UX, tools, engines, recipes, prioritization and implementation sessions. Preserve the existing four engines, 29 full tools, eight-full-tool MVP and specialist libraries unless the owner explicitly changes scope. Read [Workbench Design](docs/marketing-workbench-design.md) for F-01–F-05; Quick Tools are independently gated method-level views, not new full tools.

## Standing owner decision: capability-first dependency selection

- Evaluate and select the best technically suitable algorithms, libraries, models and components without excluding paid, commercial, dual-licensed or proprietary candidates merely because of license cost or business model. Do not ask the owner to reconfirm this policy in each session.
- Keep dependencies lean; prioritize scientific validity, fit, maintenance, security and simplicity.
- Record license terms and costs separately from technical selection. Use only authorized development/evaluation versions; obtain any permission required at development time before integrating restricted code. If not yet permitted, retain the design choice and use an independent stub/adapter or authorized alternative.
- Defer purchases required only for release/commercial operation until before that use. Release or distribution is blocked until all applicable licenses and obligations are satisfied. Never bypass licensing restrictions.
- Canonical policy: [architecture](docs/marketing-system-architecture-v1.md), section "سیاست ثابت انتخاب کتابخانه و مجوز". Applies to every engine, tool and future session.
- Maintain the four-engine, 29-tool modular monolith architecture; no unnecessary complexity.

This file records project policy, not a legal grant of permissions.

## Scientific engine implementation reference

Use [Scientific Engine & Technology Specification](docs/marketing-scientific-engine-specification.md) for all 29 tools: baseline, conditional advanced methods, dependency selection, evidence gates, fixtures and validation. Do not report PASS before actual tests; freeze compatible dependency versions in DEV.

## Scientific technology baseline and verification

- Read `docs/marketing-scientific-engine-specification.md` before selecting or changing a scientific method, library, model or API for any of the 29 tools.
- Owner-approved backend is Python 3.12 + Django; frontend React + TypeScript, DRF REST and PostgreSQL. Node is build/development only. The [development baseline](docs/marketing-development-baseline.md) and committed manifests define exact direct candidate versions, not a verified lock. Do not change the language/architecture or replace scientific libraries without owner approval and evidence.
- Proposed scientific runtime baseline is CPython 3.12.x with NumPy 2.3.5, pandas 2.3.3, SciPy 1.15.3, scikit-learn 1.9.1 and Statsmodels 0.14.5. These pins are selected from official package metadata intersections; they are not yet resolver/CI-verified. The earlier successful CI run was historical CPython 3.13.18 and does not validate this new baseline. CI credits are currently unavailable; never claim a new PASS until it is run.
- The smoke tests verify package installation/API compatibility and representative fixtures only; they do not establish scientific validity on real business data or prove all 29 tools are implemented. Persian semantic-quality benchmarks, full 29-tool golden tests, MMM/CLV sampling and causal validation remain separate gates.
- Do not add Numba as a direct StatsForecast dependency without evidence; StatsForecast 2.1.1's published dependency metadata uses coreforecast/utilsforecast. Numba is required by other optional stacks where their metadata specifies it.
- Keep Chronos-2, BERTopic, SHAP and other heavy/optional stacks lazy. Meridian 2.2.1 is the packaged MMM choice and must run in an isolated Python 3.12 environment because its ArviZ constraint conflicts with PyMC-Marketing 1.5.0; do not load model weights or execute expensive inference in the core path without a benchmark and user data/privacy review.

- Research evidence for each tool is documented in `docs/marketing-29-tools-evidence-review.md`; review it before changing a method or package. The scientific-engine specification is the runtime/API contract.


## Development freeze and execution contract

- Use one PR per VS after owner authorization, with its declared dependencies, exact approved owner-spec clauses, complete backend/API/data/UI/guide/demo/report and end-to-end acceptance. No separate frontend/backend PRs for a single capability, unnecessary fragmentation or unassigned backlog. Validate applicable method variants, not merely schema counts; review/fix in the same PR. Record actual test evidence and blockers. Do not merge with unmet hard dependencies or mark unavailable methods ready. An independent slice may proceed around an external blocker only with recorded owner approval; final VS21 requires every prior slice accepted. No new product scope or optional challenger obligation.

- Follow [Development Baseline & Architecture Freeze](docs/marketing-development-baseline.md) and the controlling [Full Product Vertical Slice Development Plan](docs/marketing-full-product-development-plan.md). Deliver the full approved product, not only the MVP. The 7 phases and 22 planned PRs VS00–VS21 assign all 72 methods, 29 full tools, 15 QT, 36 KN, 26 ST, 34 PL, 14 PO, 5 F, 11 C and 4 providers to specific delivery/acceptance owners. D3 is an intermediate MVP milestone only; D4–D6 are required. VS00 lock/compatibility is BLOCKED in the previously tested environment; VS01–21 are planned. No fabricated lockfiles or scientific PASS.
- Use `contracts/analysis.v1.schema.json` and `contracts/fixtures.v1.json`: 72 versioned methods, 24 dataset row schemas, 13 artifact types, 230 synthetic cases; all availability planned. JSON Schema validation is not semantic validation or model validity. Add full method-specific synthetic data, implementation and authorization tests before activation. Keep one registry, four engines, 29 tools and the approved MVP.
- Run `python3 scripts/verify_stack.py` on the target runtime/network, review actual resolver and test evidence before recording locks. Optional groups only as needed, Meridian isolated. Existing compatibility workflow is manual-only; do not dispatch paid CI without owner approval. 22 stdlib reference calculations passed in the historical local Python 3.13.5 environment; no new target-runtime PASS.

## Strategy Library — standing design rule
- Read [Strategy Library](docs/marketing-strategy-library.md) for the 26 strategy recipes, research evidence, implementation contract, KPI definitions and UX. Recipes compose the existing 29 tools and four engines; do not introduce a new tool, engine, database, agent or service merely for a new strategy.
- Preserve the eight-tool MVP and existing pipeline modes. Recipe availability derives from actual implemented capabilities; do not label a draft/partial strategy complete. Human approval, evidence and privacy gates remain mandatory.
- Use published research and official documentation as methodological evidence; validate the implementation with limited fixtures/API tests. Do not rerun paid CI or assert new runtime PASS for documentation changes.


## Marketing Planning Library — standing design rule
- Read [Marketing Planning Library](docs/marketing-planning-library.md) before implementing E01 or a planning recipe. 34 PL recipes reuse the 29 tools, 26 ST recipes and existing data/pipeline. E01 owns the integrated plan; no new engine, tool, database or service.
- Keep approved baseline immutable, separate forecast/actual/commitment/cash, validate resource and cost constraints independently, and require human approval. CPM is precedence-only; CP-SAT is conditional on resource constraints. No fictitious optimum or automatic external action.
- Preserve eight-tool MVP; unavailable required steps remain draft/partial. Use published evidence and limited implementation fixtures; no new CI claims or paid CI runs for these documents.

## Positioning Library — standing design rule
- Read [Brand Positioning & Mental Availability Library](docs/marketing-positioning-library.md) before implementing M06/M08, brand positioning, CEP, mental availability, distinctive assets or brand tracking. 14 PO capabilities compose existing tools; keep four engines, 29 tools, 26 ST, 34 PL and eight-tool MVP unchanged.
- Separate observed perception, desired position, estimate and hypothesis; no invented perceptual maps, universal brand score, unsupported claims, or causal inference from tracking/attribution. Enforce common survey bases, missingness, comparability, model fit, proof, approvals and privacy.
- Reuse existing scientific stack and ST05/PL13; Prince is optional candidate, not a new required dependency. Use evidence and limited code fixtures in DEV; no paid CI or runtime PASS claim for these documents.

## Workbench — standing design and acceptance rule

- Implement the 15 QT contracts and 36 starter KN entries according to the staged catalog, not a new engine. Authenticated scratch calculations and knowledge lookup must work without creating or selecting a company. Scratch inputs/results are not silently persisted; save explicitly in an authorized workspace using existing runs, snapshots and evidence gates. Never grant full-tool/pipeline readiness merely because a QT is ready.
- Knowledge definitions have a reviewed source, version, limitation and linked method/tool; no hallucinated glossary, no duplicate formula implementation, no compulsory learning path. Keep account preferences scoped to the user, public catalog IDs and allowlisted generic settings; never put company refs or analytical data into personal preferences. Reuse authorized workspace history for company analyses.
- Keep eight full tools as the provisional baseline, plus B05 basics and independently validated initial QT slices; reassess B05/B02/B04/S04/S05/E02/E03 using documented real managerial tasks and owner approval, not invented frequency or rankings. F-03 field evidence and F-05 paired workflow/time/error/comprehension/workload study are pending until actually performed. No claims of user validation, scientific performance, or CI PASS from documentation alone.

## Competitive Workbench enhancements — standing owner scope

- Read [Competitive Design Enhancements](docs/marketing-competitive-enhancements.md) for the 11 approved C-items (C-01–05, C-07–12); C-06 is excluded. Preserve 4 engines, 29 full tools, 8 full MVP, 26 ST, 34 PL, 14 PO. 15 QT, 13 initial and 2 later, with independent method readiness. No unauthenticated scratch flow.
- **Direct data connections are limited to GA4, Google Ads, Google Search Console and CRM only.** No Facebook/Meta, social, ecommerce, email, accounting or other direct connector. Manual/CSV/XLSX data is permitted with evidence/permission. CRM vendor remains pending owner selection; do not assume HubSpot. Read-only allowlists and least privilege, no provider mutation, no automatic cross-source summation or inferred person linkage.
- Template/validated synthetic demo/guide are mandatory per active method, shared schema/import. Four output formats PDF/DOCX/XLSX/PPTX use one immutable ReportViewModel with evidence, version, permissions, RTL QA. Organizational lessons are E08 artifacts, distinct from general knowledge. Profile/strategy intake requires source anchors and explicit review; imported strategy remains draft until authorized approval; prevent SSRF/prompt injection and unsafe files.
- PR01–04 pricing in B02 reuse M01/M06/B04; preference vectors/ideal points in existing PO05/PO10; Bass first-adoption model in B02; QT14/15 LTV/payback in B01; SNA in M09 from permitted relationship data, not social media scraping/connector. Enforce method prerequisites, uncertainty and independent fixtures; no new mandatory scientific dependency or runtime PASS claim. Parser/renderer and API version candidates must be resolved and tested in DEV; no paid CI solely for docs.
