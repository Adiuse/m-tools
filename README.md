# M-Tools

**Professional Marketing Workbench** — a practical workbench and external memory for professional marketing managers.

Designed for real company work and standalone everyday marketing tasks, delegating recall of definitions, frameworks and formulas while preserving conceptual understanding, strategic thinking and human judgment.

Product principles:

- Daily utility before comprehensiveness.
- Scientific depth before feature count.
- Minimum cognitive load, with understandable and inspectable results.

See the [canonical product policy and architecture (section 0)](docs/marketing-system-architecture-v1.md), [tool specifications](docs/marketing-tool-specifications.md), [UX design](docs/marketing-ux-design-v1.md) and [repository instructions](AGENTS.md).

[Workbench design](docs/marketing-workbench-design.md): Quick Tools, Marketing Knowledge Library, Professional Tools and Integrated Pipelines, with personal shortcuts, evidence-led priorities and productivity acceptance. The four engines and 29 full tools remain unchanged; individual Quick methods have their own readiness gates.

[Competitive design enhancements](docs/marketing-competitive-enhancements.md): data templates and demos, four-format executive reporting, pricing research, organization lessons, preference mapping, Bass diffusion, LTV/payback, document intake and relationship network analysis. Direct read-only connections are limited to GA4, Google Ads, Search Console and CRM (vendor pending).

[Development baseline and architecture freeze](docs/marketing-development-baseline.md): Python/Django backend, React/TypeScript frontend, PostgreSQL, direct dependency pins, [72 typed method contracts](contracts/analysis.v1.schema.json), [230 synthetic fixtures](contracts/fixtures.v1.json) and DEV roadmap.

Current status: FROZEN_DESIGN / RUNTIME_LOCK_PENDING / NOT_IMPLEMENTED. Run `python3 scripts/verify_stack.py` with the specified target runtimes and registry access to verify the candidate stack. No verified lockfiles or product validation yet. Compatibility CI is manual only.
