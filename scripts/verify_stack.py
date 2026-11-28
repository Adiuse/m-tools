"""Resolve and check the proposed baseline; run from a clean checkout.
No package changes, model downloads or paid CI dispatch are made automatically.
"""
import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".stack-check"
GROUPS = json.loads((ROOT / "deps/science-groups.json").read_text())["groups"]
PY = (ROOT / ".python-version").read_text().strip()
NODE = (ROOT / "frontend/.node-version").read_text().strip()
UV = "0.13.10"
PNPM = "11.29.0"
report = {"status":"NOT_RUN","platform":platform.platform(),"python_target":PY,"node_target":NODE,"steps":[]}
OUT.mkdir(exist_ok=True)
report_path = OUT / "report.json"


def save():
    report_path.write_text(json.dumps(report, indent=2) + "\n")


def run(label, args, cwd=ROOT, env=None, capture=False, blocked_exit_codes=()):
    args = [str(x) for x in args]
    print(f"\n--- {label}: {' '.join(args)}", flush=True)
    step = {"name":label,"command":args,"status":"RUNNING"}
    report["steps"].append(step)
    save()
    try:
        result = subprocess.run(args, cwd=cwd, env=env, check=False, text=True, stdout=subprocess.PIPE if capture else None)
    except OSError as e:
        step.update(status="BLOCKED", error=type(e).__name__)
        save()
        raise RuntimeError(f"{label}: executable unavailable") from e
    status = "PASS" if result.returncode == 0 else "FAIL"
    if result.returncode in blocked_exit_codes:
        status = "BLOCKED"
    step.update(status=status, exit_code=result.returncode)
    if capture and not result.returncode:
        step["output"] = result.stdout.strip()
    save()
    if result.returncode:
        raise RuntimeError(f"{label}: exit {result.returncode}")
    return result.stdout.strip() if capture else None


def require_version(label, cmd, expected):
    got = run(label, cmd, capture=True)
    if got != expected:
        report["steps"][-1].update(status="BLOCKED",expected=expected,actual=got)
        save()
        raise RuntimeError(f"{label}: expected {expected}, got {got}")


def project(project_dir):
    venv = project_dir / ".venv"
    env = os.environ | {"UV_PROJECT_ENVIRONMENT": str(venv)}
    lock = project_dir / "uv.lock"
    run(f"{project_dir.name} lock", ["uv","lock", *(["--check"] if lock.exists() else []),"--python",PY], project_dir, env)
    run(f"{project_dir.name} sync", ["uv","sync","--locked","--python",PY], project_dir, env)
    executable = venv / "bin/python"
    require_version(f"{project_dir.name} Python", [executable,"-c","import platform;print(platform.python_version())"], PY)
    run(f"{project_dir.name} pip check",["uv","pip","check","--python",executable])
    return executable, env


def probe(py, imports):
    run("API import probe",[py,"-c",";".join(f"import {name}" for name in imports)])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=["core","full"], default="core")
    parser.add_argument("--groups", nargs="+", choices=sorted(GROUPS))
    parser.add_argument("--meridian", action="store_true")
    args = parser.parse_args()
    if args.profile == "full" and args.groups:
        parser.error("Use either --profile full or --groups, not both")
    groups = sorted(GROUPS if args.profile == "full" else set(args.groups or []))
    meridian = args.profile == "full" or args.meridian
    report.update(profile=args.profile, groups=groups, meridian=meridian)
    report["commit"] = run("Git revision", ["git", "rev-parse", "HEAD"], capture=True)
    if sys.platform != "linux" or platform.machine() != "x86_64":
        raise RuntimeError("Target is Linux x86_64; other platforms are not verified")
    uv_version = run("uv",["uv","--version"],capture=True)
    if uv_version.split()[:2] != ["uv",UV]:
        report["steps"][-1].update(status="BLOCKED",expected=UV,actual=uv_version)
        save()
        raise RuntimeError(f"Expected uv {UV}, got {uv_version}")
    require_version("Node",["node","--version"],f"v{NODE}")
    require_version("pnpm",["pnpm","--version"],PNPM)
    py, env = project(ROOT)
    run("reference arithmetic",[py,ROOT/"tests/reference_calculations.py"])
    run("contract schema",[py,ROOT/"tests/contract_schema_check.py"])
    probe(py,["django","rest_framework","psycopg","pydantic","jsonschema","pandera","networkx","openpyxl","xlsxwriter","docx","pptx","pypdf","defusedxml"])
    run("core science API",[py,ROOT/"tests/scientific_stack_smoke.py","core"])
    frontend = ROOT/"frontend"
    if not (frontend/"pnpm-lock.yaml").exists():
        run("frontend lock",["pnpm","install","--lockfile-only"],frontend)
    run("frontend frozen install",["pnpm","install","--frozen-lockfile"],frontend)
    run("TypeScript CLI",["pnpm","exec","tsc","--version"],frontend)
    run("Vite CLI",["pnpm","exec","vite","--version"],frontend)
    run("PostgreSQL connectivity and transactions", [py, ROOT / "tests/postgres_stack_smoke.py"], blocked_exit_codes=(2,))
    if groups:
        constraints = OUT/"core-constraints.txt"
        run("export core pins",["uv","export","--locked","--no-dev","--no-hashes","--no-emit-project","-o",constraints],env=env)
        name = "+".join(groups)
        inputs = OUT/(name+".in")
        inputs.write_text("\n".join(req for group in groups for req in GROUPS[group])+"\n")
        locks = ROOT/"deps/locks"
        locks.mkdir(exist_ok=True)
        candidate = OUT/(name+".txt")
        lock = locks/(name+".txt")
        # Recompile against the verified core lock on every check, but do not silently replace a committed lock.
        if not lock.exists():
            run("resolve combined science",["uv","pip","compile",ROOT/"pyproject.toml",inputs,"-c",constraints,"--python",py,"--generate-hashes","-o",candidate])
        else:
            candidate = lock
        venv = OUT/"science-venv"
        run("isolated science test venv",["uv","venv","--clear","--python",py,venv])
        science_py = venv/"bin/python"
        run("install locked science",["uv","pip","sync","--python",science_py,"--require-hashes",candidate])
        run("combined dependency check",["uv","pip","check","--python",science_py])
        # Check both the core freeze and every direct optional pin against the installed combination.
        pins = [line.split(" #")[0].strip() for line in constraints.read_text().splitlines() if "==" in line and not line.startswith(("#"," ","-"))]
        pins += [req for g in groups for req in GROUPS[g]]
        run("verify locked versions",[science_py,"-c","import sys; from importlib.metadata import version; from packaging.requirements import Requirement; reqs=[Requirement(p) for p in sys.argv[1:]]; assert all((r.marker and not r.marker.evaluate()) or r.specifier.contains(version(r.name),prereleases=True) for r in reqs)",*pins])
        suites = {"forecast","causal","bayesian","optimization","analytics","ml","nlp"}
        run("combined core API",[science_py,ROOT/"tests/scientific_stack_smoke.py","core"])
        for group in groups:
            if group in suites:
                run(f"{group} API",[science_py,ROOT/"tests/scientific_stack_smoke.py",group])
        extra = {"survey":["svy"],"choice":["biogeme"],"monitoring":["ruptures"],"ml":["lifelines"],"optimization":["pymcdm"]}
        for group in groups:
            if group in extra:
                probe(science_py,extra[group])
        if not lock.exists():
            lock.write_bytes(candidate.read_bytes())
    if meridian:
        meridian_py, _ = project(ROOT/"deps/meridian")
        run("Meridian API",[meridian_py,ROOT/"tests/scientific_stack_smoke.py","meridian"])
    report["status"] = "PASS"
    print("PASS: selected installation, API, contract, and PostgreSQL transaction checks.")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, OSError, ValueError) as exc:
        report["status"] = "BLOCKED" if not report["steps"] or any(s["status"]=="BLOCKED" for s in report["steps"]) else "FAIL"
        report["error"] = str(exc)
        print(report["error"],file=sys.stderr)
        sys.exit(1)
    finally:
        locks = [ROOT / "uv.lock", ROOT / "frontend/pnpm-lock.yaml", ROOT / "deps/meridian/uv.lock"]
        locks.extend(sorted((ROOT / "deps/locks").glob("*.txt")))
        report["lock_sha256"] = {
            str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in locks if path.is_file()
        }
        save()
