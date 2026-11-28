# VS01 workbench development

VS01 implements the workbench foundation defined in [Full Product Plan §4](marketing-full-product-development-plan.md), [Development Baseline §§3–4](marketing-development-baseline.md), [Architecture §§2, 4, 5, 8](marketing-system-architecture-v1.md) and [UX §§2–3](marketing-ux-design-v1.md). All 72 catalog methods, covering 29 professional tools and 15 quick tools, remain planned. Preflight checks the request and references and shows the method's requirements and limitations. Calculations and tool activation belong to their delivery slices.

## Run locally

Use the VS00 toolchain and an isolated PostgreSQL 17 development database named `mtools`. Provide its connection settings with `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER` and `PGPASSWORD` as needed.

```sh
uv sync --locked
pnpm --dir frontend install --frozen-lockfile
pnpm --dir frontend build
export MTOOLS_DEBUG=1
export MTOOLS_PUBLIC_ORIGIN=http://127.0.0.1:8000
uv run --locked python backend/manage.py migrate
uv run --locked python backend/manage.py runserver 127.0.0.1:8000
```

Open http://127.0.0.1:8000. Create an account, open the activation link printed in the development console, then choose a password and sign in. The console also receives local password-reset links. For a Vite development server, use `pnpm --dir frontend dev` with Django on port 8000, and set the public origin to the Vite URL. Vite proxies API requests to Django.

Create two workspaces. In one workspace, add an evidence entry, revise it, and open its earlier version. Use one of those evidence versions to record a manual numeric series with dated entries. Open History to see the saved changes, return to the workbench, and open the other workspace. In the first workspace, select a planned professional tool, enter a question and inspect its requirements. Save a draft, reload, and open the saved draft. Quick tools can be inspected from the personal catalog without selecting a workspace. Their scratch endpoint validates the request and returns planned status without storing inputs.

In a deployed environment set `MTOOLS_SECRET_KEY`, `MTOOLS_ALLOWED_HOSTS`, `MTOOLS_PUBLIC_ORIGIN` (HTTPS), database credentials and the SMTP variables in Django settings. Configure the HTTPS WSGI service and serve the built `/assets/` files from the same origin. The production settings use secure cookies and SMTP. Development settings use an HTTP loopback and the console mail backend.

## Data and execution

- Workspace rights come from active membership. Owners manage membership and approve decisions, editors change records and save analysis drafts, and viewers read workspace records. Drafts are private to their creator.
- Record revisions create a new row and UUID, retain the series ID and increment the version. PATCH accepts changed fields and uses the version in the URL as its base. A stale base returns HTTP 409.
- Dataset requests use `DatasetPayload` v1 inside `{title, payload}`, where scope and evidence references identify the exact source versions. The manual UI supports numeric series. The API validates dataset envelopes and scoped references. CSV/XLSX import and executive export routes are delivered in VS02.
- Analysis draft, preflight and run requests use `RunRequest` v1. The scratch endpoint accepts `ScratchRequest` v1. The registered catalog controls availability. Server-side queue primitives claim jobs atomically, expire leases, limit retries and validate terminal results before committing them.
- PostgreSQL composite foreign keys enforce workspace ownership of linked rows. Versioned records and completed run snapshots are protected against in-place updates. Job retries preserve the original input snapshot. Approving a decision is a separate, owner-only request.
- Keep database backups before production migration. In a development database, `migrate core 0001` reverses the workspace constraints and triggers in migration 0002. A subsequent `migrate` restores them.

## Acceptance commands

```sh
uv run --locked python backend/manage.py makemigrations --check --dry-run
uv run --locked python backend/manage.py test core
pnpm --dir frontend build
```

For browser acceptance, run `node frontend/workbench.e2e.mjs` against a development server with a disposable test account. Set `MTOOLS_TEST_EMAIL` and `MTOOLS_TEST_PASSWORD` for that account. Use a local Playwright with Chromium installed and set `PLAYWRIGHT_MODULE` to the Playwright module path if needed. `MTOOLS_BROWSER_URL` defaults to the loopback server above. The test creates isolated, timestamped synthetic workspaces in the development database.
