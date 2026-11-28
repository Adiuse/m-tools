"""Validate the contract and fixture structure, not the application or model fits."""
import json
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
schema = json.loads((ROOT / "contracts/analysis.v1.schema.json").read_text())
fixtures = json.loads((ROOT / "contracts/fixtures.v1.json").read_text())["cases"]
catalog = schema["x-method-catalog"]
defs = schema["$defs"]
Draft202012Validator.check_schema(schema)


def validator(ref):
    return Draft202012Validator(
        {**schema, "$ref": ref}, format_checker=FormatChecker()
    )


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def walk(value):
    if isinstance(value, dict):
        if "$ref" in value:
            ref = value["$ref"]
            check(ref.startswith("#/$defs/") and ref[8:] in defs, f"Unknown ref: {ref}")
        for child in value.values():
            walk(child)
    elif isinstance(value, list):
        for child in value:
            walk(child)


walk(schema)
methods = {(m["method_id"], m["method_version"]): m for m in catalog}
check(len(methods) == len(catalog), "Duplicate method/version")
expected_owners = {f"{prefix}{i:02}" for prefix, end in [("S",6),("M",9),("B",6),("E",8)] for i in range(1,end+1)}
check({m["tool_id"] for m in catalog} == expected_owners, "Owner coverage")
check({m["method_id"] for m in catalog if m["quick"]} == {f"QT{i:02}" for i in range(1,16)}, "Quick tools")
check(len([name for name in defs if name.startswith("Row_")]) == 24, "Dataset row schemas")
check(len(defs["ArtifactEnvelope"]["oneOf"]) == 13, "Artifact types")
check(set(defs["Connection"]["properties"]["provider"]["enum"]) == {"GA4","GOOGLE_ADS","SEARCH_CONSOLE","CRM"}, "Connector scope")

ids = set()
seen = Counter()
wid = "00000000-0000-4000-8000-000000000001"
rid = "00000000-0000-4000-8000-000000000002"
request_validator = validator("#/$defs/RunRequest")
result_validator = validator("#/$defs/RunResult")
scratch_validator = validator("#/$defs/ScratchRequest")
scratch_result_validator = validator("#/$defs/ScratchResult")
for case in fixtures:
    cid = case["id"]
    check(cid not in ids, f"Duplicate fixture {cid}")
    ids.add(cid)
    key = (case["method_id"], case["method_version"])
    method = methods[key]
    check(case["tool_id"] == method["tool_id"] and case["synthetic"] is True, cid)
    seen[key, case["case"]] += 1
    invalid = case["case"] == "invalid_input"
    common = dict(tool_id=method["tool_id"], method_id=key[0], method_version=key[1])
    req = dict(**common, workspace_id=wid, question="Synthetic fixture", input=case["input"], evidence_refs=[], dependency_run_ids=[], idempotency_key=cid)
    check(validator(method["input_ref"]).is_valid(case["input"]) != invalid, f"Input: {cid}")
    check(request_validator.is_valid(req) != invalid, f"Envelope: {cid}")
    if method["quick"]:
        scratch = dict(quick_id=key[0], method_version=key[1], input=case["input"])
        check(scratch_validator.is_valid(scratch) != invalid, f"Scratch: {cid}")
    expected = case["expected"]
    if "output" in expected:
        validator(method["output_ref"]).validate(expected["output"])
        result = dict(**common, run_id=rid, workspace_id=wid, status="succeeded", analysis_status=expected["analysis_status"], input_hash="0"*64, findings=[], options=[], assumptions=[], evidence_refs=[], limitations=[], missing_fields=[], output=expected["output"], next_action=None, error_code=None)
        result_validator.validate(result)
        if method["quick"]:
            scratch_result_validator.validate({k:v for k,v in result.items() if k in {"method_version","analysis_status","input_hash","output","assumptions","limitations","missing_fields","error_code"}} | {"quick_id":key[0]})
    if "assert_fields" in expected:
        properties = defs[method["output_ref"].split("/")[-1]]["properties"]
        for field, value in expected["assert_fields"].items():
            check(field in properties, f"Unknown output field: {cid}.{field}")
            Draft202012Validator({**schema, "$ref": method["output_ref"] + "/properties/" + field}, format_checker=FormatChecker()).validate(value)
    if invalid:
        check(expected["http_status"] == 422, cid)
for key in methods:
    for kind in ("reference","missing_data","invalid_input"):
        check(seen[key,kind] == 1, f"Missing/duplicate {key} {kind}")
print(f"PASS: structural validation only; {len(expected_owners)} owners, {len(catalog)} methods, {len(fixtures)} fixtures")
