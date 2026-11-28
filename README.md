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

[Full-product development plan](docs/marketing-full-product-development-plan.md): 7 phases, 22 planned PRs (VS00–VS21), 19 capability-oriented delivery slices, explicit coverage and acceptance of the complete approved product. The eight-tool MVP is an intermediate milestone, not the final deliverable.

VS00 records the core backend and frontend lockfiles. Local verification passed on Linux x86_64 with CPython 3.12.16, Node 24.22.3 and PostgreSQL 17.12. See the [development baseline](docs/marketing-development-baseline.md#۵-gate-سازگاری-و-اجرای-محلی) for the verification command and database settings. Product implementation starts in VS01 after VS00 acceptance. Compatibility CI is manual only.
