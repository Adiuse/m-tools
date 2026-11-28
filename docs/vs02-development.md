# VS02 development and verification

VS02 implements shared data and document intake and executive reporting from the [vertical slice plan](marketing-full-product-development-plan.md) and [C-01, C-02 and C-10](marketing-competitive-enhancements.md). VS01 is the merged prerequisite. Method availability continues to come from the v1 registry.

## Run and exercise the slice

Start the [workbench](workbench-development.md) with the approved VS00 dependency locks and migrate the database. Start a second local process with the same Django settings and database:

```sh
export MTOOLS_PDF_CHROMIUM=/path/to/chromium
uv run --locked python backend/manage.py process_exports --watch
```

Use a Chromium executable with the sandbox available to the worker. Acceptance testing uses Chromium with its sandbox enabled. A production release needs its own pinned renderer and isolated runtime configuration.

1. Open Import file in a workspace with source evidence. Download the schema-derived CSV or Excel template, enter the scope and source version, and stage a file. Inspect accepted rows, download errors where available, and confirm the file checksum to save a version. The provided numeric example requires the synthetic designation.
2. Open Profile source. Supply a permitted file or a direct public HTTPS page that permits intake in its robots file. Review only explicitly sourced fields with their anchors, select the ones to apply, and confirm against the current profile version. The updated version and source evidence are written atomically.
3. Open Reports, choose a dataset or saved report version, language, format and template. Use the worker to generate and download PDF, Word, Excel or PowerPoint. Exports for different formats share a frozen ReportViewModel and display data for the selected source version. A newer dataset version is shown separately so the original download remains reproducible.

## Evidence and review status

- CSV/XLSX and profile staging are workspace- and user-scoped. Confirming a preview is explicit. Tests cover Persian numeric normalization, missing versus zero, error rows, Excel formula rejection, ZIP macros, synthetic provenance and a stale profile guard.
- Export coverage uses a Persian synthetic dataset with values 70, 100 and missing. All four files are reopened by format-specific readers and checked for values and source provenance. A shared checksum, stale source and revoked access are exercised. PDF and PowerPoint are rendered for visual review with Chromium and LibreOffice; Word and Excel remain editable OOXML.
- The direct HTTPS path rejects non-public DNS answers before connecting and uses the numeric address with the original hostname for TLS. Redirects require a new explicitly selected direct URL. Local tests cover the public pin, private-address rejection and redirect refusal.
- The generic dataset report is labeled draft or demo. Its table and chart sections are rendered from immutable source versions.

## Acceptance follow-up

- Reports can now start with a saved `ReportViewModel` or an immutable dataset version. Table and chart data are frozen with the report. Numeric line and column charts are rendered in PDF and remain editable Excel and PowerPoint charts. Word and unsupported chart types retain the source value tables. Downloads expire after one hour. The worker periodically prunes expired files and checks the creator's workspace permission before rendering.
- The profile review also supports explicit company name, audience, channel, public contact and pricing terms. Conflicting values within a source stay pending. A separate, bounded parser process receives file bytes with a reduced environment. It applies local CPU, memory, file size and elapsed-time limits. The deterministic parser uses named fields and source anchors.
- The method example endpoint lists the checked synthetic numeric-series sample for methods bound to that schema and identifies remaining examples as planned. Method-specific fixture completion belongs to the corresponding implementation slice.
- Chromium 151.0.7922.34 rendered the local fixture with its sandbox enabled. This run does not establish deployment permission or renderer compliance for a production host.
- Live HTTPS was attempted through the actual pinned-fetch path against a public documentation site. In this execution environment, DNS resolution failed before a socket connection. The private address, redirect and DNS pin tests exercise the local implementation. A reachable approved page and the deployment environment are still needed for live production acceptance.

## Static conformance review of VS01 and VS02

| Design clause | Conformance correction and local regression coverage |
|---|---|
| VS01 and Architecture §4. Preserve observational provenance and comparable input scopes. | Shared checks reject observed findings without eligible evidence and observations derived from synthetic input. Profile-source assertions are tagged separately and retain that tag on revisions. Numeric data uses consistent units, periods and series currency. Observation versions keep the same metric, period and dimensional grain. |
| C-01. Typed row validation, explicit mapping, immutable staged intake. | CSV/XLSX conversion preserves strings, booleans, missing values and zeros. Native Excel timestamps use the explicitly selected IANA timezone, with ambiguous times requiring an offset. Semantic row failures are included in the error report. Confirming via the dataset API requires the exact staged mapping, source checksum and template version. PostgreSQL guards staged data against edits and cross-workspace application. |
| C-02. Traceable exports from a common immutable snapshot. | The snapshot records dataset and per-row evidence versions. The worker and download route recheck those references and access. Demo sources cannot be relabeled final. Renderers expose truncated previews, keep raw Excel dates and large integer precision, record renderer metadata, and render visible source context and KPI currencies. |
| C-10. Explicit, independently reviewable profile claims. | The parser joins visible inline page text and ignores script/style content. Currency and dates are validated against profile fields. Approval writes the v1 `DraftImportResult` contract with evidence hash, source anchors, explicit decisions and applied version. The accepted profile and source claim are written together. |
| Delivery boundaries. | Catalog methods remain planned until their owning slices are accepted. VS01/VS02 local checks cover the shared foundation. Live external intake and production-host deployment tests are outside this static review. |
