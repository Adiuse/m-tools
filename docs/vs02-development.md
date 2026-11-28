# VS02 development and verification

VS02 implements shared data and document intake and executive reporting from the [vertical slice plan](marketing-full-product-development-plan.md) and [C-01, C-02 and C-10](marketing-competitive-enhancements.md). VS01 is the merged prerequisite. Method availability continues to come from the v1 registry.

## Run and exercise the slice

Start the [workbench](workbench-development.md) with the approved VS00 dependency locks and migrate the database. Start a second local process with the same Django settings and database:

```sh
export MTOOLS_PDF_CHROMIUM=/path/to/chromium
uv run --locked python backend/manage.py process_exports --watch
```

Use a Chromium executable with the sandbox available to the worker. The isolated development fixture used the pinned test shell and explicitly opted out of the Chromium sandbox under `MTOOLS_DEBUG=1`. A production release needs its own pinned renderer and isolated runtime configuration.

1. Open Import file in a workspace with source evidence. Download the schema-derived CSV or Excel template, enter the scope and source version, and stage a file. Inspect accepted rows, download errors where available, and confirm the file checksum to save a version. The provided numeric example requires the synthetic designation.
2. Open Profile source. Supply a permitted file or a direct public HTTPS page that permits intake in its robots file. Review only explicitly sourced fields with their anchors, select the ones to apply, and confirm against the current profile version. The updated version and source evidence are written atomically.
3. Open Reports, choose a dataset version, language, format and template. Use the worker to generate and download PDF, Word, Excel or PowerPoint. Exports for different formats share a frozen ReportViewModel and display data for the selected source version. A newer dataset version is shown separately so the original download remains reproducible.

## Evidence and review status

- CSV/XLSX and profile staging are workspace- and user-scoped. Confirming a preview is explicit. Tests cover Persian numeric normalization, missing versus zero, error rows, Excel formula rejection, ZIP macros, synthetic provenance and a stale profile guard.
- Export coverage uses a Persian synthetic dataset with values 70, 100 and missing. All four files are reopened by format-specific readers and checked for values and source provenance. A shared checksum, stale source and revoked access are exercised. PDF and PowerPoint are rendered for visual review with Chromium and LibreOffice; Word and Excel remain editable OOXML.
- The direct HTTPS path rejects non-public DNS answers before connecting and uses the numeric address with the original hostname for TLS. Redirects require a new explicitly selected direct URL. Local tests cover the public pin, private-address rejection and redirect refusal.
- This draft provides the checked numeric-series example and registry-based tabular templates. Complete examples for each method, richer chart and artifact-specific report rendering, additional profile field mappings, and live authorized website intake with production isolation remain acceptance work. The generic report path reads immutable dataset versions. The executive output is labeled draft or demo.
