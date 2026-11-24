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
