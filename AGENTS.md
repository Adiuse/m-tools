# M-Tools repository instructions

Read the architecture and tool specification documents before making design or implementation decisions.

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
- Proposed scientific runtime baseline is CPython 3.12.x with NumPy 2.3.5, pandas 2.3.3, SciPy 1.15.3, scikit-learn 1.9.1 and Statsmodels 0.14.5. These pins are selected from official package metadata intersections; they are not yet resolver/CI-verified. The earlier successful CI run was historical CPython 3.13.18 and does not validate this new baseline. CI credits are currently unavailable; never claim a new PASS until it is run.
- The smoke tests verify package installation/API compatibility and representative fixtures only; they do not establish scientific validity on real business data or prove all 29 tools are implemented. Persian semantic-quality benchmarks, full 29-tool golden tests, MMM/CLV sampling and causal validation remain separate gates.
- Do not add Numba as a direct StatsForecast dependency without evidence; StatsForecast 2.1.1's published dependency metadata uses coreforecast/utilsforecast. Numba is required by other optional stacks where their metadata specifies it.
- Keep Chronos-2, BERTopic, SHAP and other heavy/optional stacks lazy. Meridian 2.2.1 is the packaged MMM choice and must run in an isolated Python 3.12 environment because its ArviZ constraint conflicts with PyMC-Marketing 1.5.0; do not load model weights or execute expensive inference in the core path without a benchmark and user data/privacy review.

- Research evidence for each tool is documented in `docs/marketing-29-tools-evidence-review.md`; review it before changing a method or package. The scientific-engine specification is the runtime/API contract.


## Strategy Library — standing design rule
- Read [Strategy Library](docs/marketing-strategy-library.md) for the 26 strategy recipes, research evidence, implementation contract, KPI definitions and UX. Recipes compose the existing 29 tools and four engines; do not introduce a new tool, engine, database, agent or service merely for a new strategy.
- Preserve the eight-tool MVP and existing pipeline modes. Recipe availability derives from actual implemented capabilities; do not label a draft/partial strategy complete. Human approval, evidence and privacy gates remain mandatory.
- Use published research and official documentation as methodological evidence; validate the implementation with limited fixtures/API tests. Do not rerun paid CI or assert new runtime PASS for documentation changes.
