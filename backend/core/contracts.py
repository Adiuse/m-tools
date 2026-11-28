import hashlib
import json

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from jsonschema import Draft202012Validator, FormatChecker

SCHEMA = json.loads((settings.ROOT / "contracts/analysis.v1.schema.json").read_text())
CATALOG = tuple(SCHEMA["x-method-catalog"])
METHODS = {(entry["method_id"], entry["method_version"]): entry for entry in CATALOG}
CHECKER = FormatChecker()


def schema_for(name):
    return {"$ref": f"#/$defs/{name}", "$defs": SCHEMA["$defs"]}


def validate(name, payload):
    validator = Draft202012Validator(schema_for(name), format_checker=CHECKER)
    return next(validator.iter_errors(payload), None)


def digest(data):
    canonical = json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":"),
                           allow_nan=False, cls=DjangoJSONEncoder)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
