from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from rest_framework import serializers

from . import models


class StrictSerializer(serializers.Serializer):
    def to_internal_value(self, data):
        if isinstance(data, dict):
            unknown = set(data) - set(self.fields)
            if unknown:
                raise serializers.ValidationError({key: "Unknown field." for key in sorted(unknown)})
        return super().to_internal_value(data)


class WorkspaceInput(StrictSerializer):
    name = serializers.CharField(max_length=160)
    currency = serializers.RegexField(r"^[A-Z]{3}$")
    timezone = serializers.CharField(max_length=64)
    industry = serializers.CharField(max_length=160)
    offering = serializers.CharField(max_length=200)
    objective = serializers.CharField(max_length=400)

    def validate_timezone(self, value):
        try:
            ZoneInfo(value)
        except (ValueError, ZoneInfoNotFoundError):
            raise serializers.ValidationError("Use an IANA timezone.") from None
        return value


class ProfileInput(StrictSerializer):
    industry = serializers.CharField(max_length=160)
    offering = serializers.CharField(max_length=200)
    objective = serializers.CharField(max_length=400)
    business_model = serializers.CharField(max_length=200, allow_blank=True, required=False)
    geography = serializers.CharField(max_length=160, allow_blank=True, required=False)
    company_name = serializers.CharField(max_length=160, allow_blank=True, required=False)
    target_segment = serializers.CharField(max_length=200, allow_blank=True, required=False)
    channels = serializers.CharField(max_length=240, allow_blank=True, required=False)
    public_contact = serializers.CharField(max_length=240, allow_blank=True, required=False)
    pricing_terms = serializers.CharField(max_length=400, allow_blank=True, required=False)
    constraints = serializers.ListField(child=serializers.CharField(max_length=500), max_length=100, required=False)


class EvidenceInput(StrictSerializer):
    kind = serializers.ChoiceField(choices=models.Evidence._meta.get_field("kind").choices)
    title = serializers.CharField(max_length=200)
    source_uri = serializers.URLField(max_length=200, allow_blank=True, required=False)
    collected_at = serializers.DateField()
    period_start = serializers.DateField(allow_null=True, required=False)
    period_end = serializers.DateField(allow_null=True, required=False)
    scope = serializers.CharField(max_length=200, allow_blank=True, required=False)
    quality_notes = serializers.CharField(max_length=2000, allow_blank=True, required=False)
    sensitivity = serializers.ChoiceField(choices=["internal", "restricted"], required=False)

    def validate_source_uri(self, value):
        if value and not value.lower().startswith(("https://", "http://")):
            raise serializers.ValidationError("Use an HTTP(S) source address.")
        return value

    def validate(self, data):
        start, end = data.get("period_start"), data.get("period_end")
        if (start is not None or end is not None) and (start is None or end is None or start >= end):
            raise serializers.ValidationError({"period_end": "Specify an exclusive end after the start."})
        return data


class DatasetInput(StrictSerializer):
    title = serializers.CharField(max_length=200)
    payload = serializers.JSONField()


class MetricInput(StrictSerializer):
    key = serializers.SlugField(max_length=50)
    definition = serializers.CharField(max_length=400)
    unit = serializers.CharField(max_length=40)
    grain = serializers.CharField(max_length=60)
    formula_id = serializers.CharField(max_length=64, allow_blank=True, required=False)
    direction = serializers.ChoiceField(choices=["increase", "decrease", "target"])
    window_rule = serializers.CharField(max_length=160, allow_blank=True, required=False)


class ObservationInput(StrictSerializer):
    metric_id = serializers.UUIDField()
    dataset_id = serializers.UUIDField(allow_null=True, required=False)
    evidence_id = serializers.UUIDField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()
    dimensions = serializers.DictField(child=serializers.CharField(max_length=160), required=False)
    value = serializers.DecimalField(max_digits=38, decimal_places=12, allow_null=True)
    currency = serializers.RegexField(r"^[A-Z]{3}$", allow_blank=True, required=False)
    missing_reason = serializers.CharField(max_length=160, allow_blank=True, required=False)

    def validate(self, data):
        if data["period_start"] >= data["period_end"]:
            raise serializers.ValidationError({"period_end": "Specify an exclusive end after the start."})
        if (data["value"] is None) != bool(data.get("missing_reason")):
            raise serializers.ValidationError({"missing_reason": "Required for missing values only."})
        return data


class GoalInput(StrictSerializer):
    metric_id = serializers.UUIDField()
    baseline_id = serializers.UUIDField(allow_null=True, required=False)
    target = serializers.DecimalField(max_digits=38, decimal_places=12)
    deadline = serializers.DateField()


class HypothesisInput(StrictSerializer):
    statement = serializers.CharField(max_length=600)
    evidence_id = serializers.UUIDField(allow_null=True, required=False)


class MembershipInput(StrictSerializer):
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=models.Membership.Role.choices)
    active = serializers.BooleanField(default=True)


class DecisionInput(StrictSerializer):
    run_id = serializers.UUIDField()
    selected_option = serializers.CharField(max_length=160)
    reason = serializers.CharField(max_length=500)


class ActionInput(StrictSerializer):
    decision_id = serializers.UUIDField()
    owner_id = serializers.UUIDField()
    goal_id = serializers.UUIDField(allow_null=True, required=False)
    title = serializers.CharField(max_length=200)
    due_date = serializers.DateField()
    planned_cost = serializers.DecimalField(max_digits=26, decimal_places=8, min_value=0)
    currency = serializers.RegexField(r"^[A-Z]{3}$")


class OutcomeInput(StrictSerializer):
    action_id = serializers.UUIDField()
    observation_id = serializers.UUIDField()
    interpretation = serializers.CharField(max_length=500)
