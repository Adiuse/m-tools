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
- Scientific runtime baseline is CPython 3.12.x. Candidate pins are not considered validated until the `Scientific stack compatibility` GitHub Actions workflow passes.
- The smoke tests verify package installation/API compatibility only; they do not establish scientific validity on real business data. Persian model-weight benchmarks and MMM/CLV/causal empirical validation remain separate gates.
- Do not add Numba as a direct StatsForecast dependency without evidence; StatsForecast 2.1.1's published dependency metadata uses coreforecast/utilsforecast. Numba is required by other optional stacks where their metadata specifies it.
- Keep Chronos-2, Meridian, BERTopic, SHAP and other heavy/optional stacks as conditional challengers; do not load model weights or execute expensive inference in the core path without a benchmark and user data/privacy review.
