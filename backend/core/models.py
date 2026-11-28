import uuid

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.db.models import Q


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **fields):
        if not email:
            raise ValueError("Email is required.")
        user = self.model(email=email.strip().lower(), **fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **fields):
        return self.create_user(email, password, **{**fields, "is_staff": True, "is_superuser": True})


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()


class Workspace(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=160)
    currency = models.CharField(max_length=3)
    timezone = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)


class Membership(models.Model):
    class Role(models.TextChoices):
        OWNER = "owner"
        EDITOR = "editor"
        VIEWER = "viewer"

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=6, choices=Role)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["workspace", "user"], name="membership_workspace_user"),
            models.CheckConstraint(condition=Q(role__in=["owner", "editor", "viewer"]), name="membership_role_valid"),
        ]


class TenantRow(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        unique_together = [("workspace", "id")]


class Versioned(TenantRow):
    series = models.UUIDField(default=uuid.uuid4, editable=False)
    version = models.PositiveIntegerField(default=1)

    class Meta(TenantRow.Meta):
        abstract = True
        unique_together = [("workspace", "id"), ("workspace", "series", "version")]


class CompanyProfile(Versioned):
    industry = models.CharField(max_length=160)
    offering = models.CharField(max_length=200)
    objective = models.CharField(max_length=400)
    business_model = models.CharField(max_length=200, blank=True)
    geography = models.CharField(max_length=160, blank=True)
    company_name = models.CharField(max_length=160, blank=True, default="")
    target_segment = models.CharField(max_length=200, blank=True, default="")
    channels = models.CharField(max_length=240, blank=True, default="")
    public_contact = models.CharField(max_length=240, blank=True, default="")
    pricing_terms = models.CharField(max_length=400, blank=True, default="")
    pricing_currency = models.CharField(max_length=3, blank=True, default="")
    pricing_date = models.DateField(null=True, blank=True)
    constraints = models.JSONField(default=list)


class Evidence(Versioned):
    claim_only = models.BooleanField(default=False)
    kind = models.CharField(max_length=16, choices=[(x, x) for x in ("internal", "primary", "secondary", "assumption")])
    title = models.CharField(max_length=200)
    source_uri = models.URLField(blank=True)
    collected_at = models.DateField()
    period_start = models.DateField(null=True)
    period_end = models.DateField(null=True)
    scope = models.CharField(max_length=200, blank=True)
    quality_notes = models.TextField(blank=True)
    sensitivity = models.CharField(max_length=16, choices=[(x, x) for x in ("internal", "restricted")], default="internal")
    checksum = models.CharField(max_length=64)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class Dataset(Versioned):
    title = models.CharField(max_length=200)
    evidence = models.ForeignKey(Evidence, on_delete=models.PROTECT)
    schema_id = models.CharField(max_length=64)
    schema_version = models.PositiveIntegerField()
    checksum = models.CharField(max_length=64)
    row_count = models.PositiveIntegerField()
    payload = models.JSONField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)


class MetricDefinition(Versioned):
    key = models.SlugField()
    definition = models.CharField(max_length=400)
    unit = models.CharField(max_length=40)
    grain = models.CharField(max_length=60)
    formula_id = models.CharField(max_length=64, blank=True)
    direction = models.CharField(max_length=12, choices=[(x, x) for x in ("increase", "decrease", "target")])
    window_rule = models.CharField(max_length=160, blank=True)


class Observation(Versioned):
    metric = models.ForeignKey(MetricDefinition, on_delete=models.PROTECT)
    dataset = models.ForeignKey(Dataset, null=True, on_delete=models.PROTECT)
    evidence = models.ForeignKey(Evidence, on_delete=models.PROTECT)
    period_start = models.DateField()
    period_end = models.DateField()
    dimensions = models.JSONField(default=dict)
    dimensions_hash = models.CharField(max_length=64)
    value = models.DecimalField(max_digits=38, decimal_places=12, null=True)
    currency = models.CharField(max_length=3, blank=True)
    missing_reason = models.CharField(max_length=160, blank=True)

    class Meta(Versioned.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "metric", "period_start", "period_end", "dimensions_hash", "version"],
                name="observation_grain_version",
            ),
            models.CheckConstraint(condition=Q(period_end__gt=models.F("period_start")), name="observation_period_order"),
        ]


class Goal(Versioned):
    metric = models.ForeignKey(MetricDefinition, on_delete=models.PROTECT)
    baseline = models.ForeignKey(Observation, null=True, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    target = models.DecimalField(max_digits=38, decimal_places=12)
    deadline = models.DateField()


class Hypothesis(Versioned):
    statement = models.CharField(max_length=600)
    evidence = models.ForeignKey(Evidence, null=True, on_delete=models.PROTECT)


class RunDraft(Versioned):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    request = models.JSONField()
    idempotency_key = models.CharField(max_length=120)
    input_hash = models.CharField(max_length=64)

    class Meta(Versioned.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "creator", "idempotency_key"], name="draft_creator_idempotency",
            )
        ]


class AnalysisRun(TenantRow):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    tool_id = models.CharField(max_length=8)
    method_id = models.CharField(max_length=80)
    method_version = models.PositiveIntegerField()
    idempotency_key = models.CharField(max_length=120)
    input_snapshot = models.JSONField()
    input_hash = models.CharField(max_length=64)
    status = models.CharField(max_length=12, default="queued")
    result = models.JSONField(null=True)

    class Meta(TenantRow.Meta):
        constraints = [
            models.UniqueConstraint(fields=["workspace", "idempotency_key"], name="run_workspace_idempotency"),
            models.CheckConstraint(condition=Q(status__in=["queued", "running", "succeeded", "failed"]), name="run_status_valid"),
            models.CheckConstraint(
                condition=(Q(status__in=["queued", "running"], result__isnull=True)
                           | Q(status__in=["succeeded", "failed"], result__isnull=False)),
                name="run_result_matches_lifecycle",
            ),
        ]


class Job(TenantRow):
    run = models.OneToOneField(AnalysisRun, on_delete=models.CASCADE)
    available_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)
    lease_token = models.UUIDField(null=True)
    lease_until = models.DateTimeField(null=True)

    class Meta(TenantRow.Meta):
        constraints = [
            models.CheckConstraint(
                condition=(Q(lease_token__isnull=True, lease_until__isnull=True)
                           | Q(lease_token__isnull=False, lease_until__isnull=False)),
                name="job_lease_fields_paired",
            ),
        ]


class Artifact(Versioned):
    run = models.ForeignKey(AnalysisRun, on_delete=models.PROTECT)
    artifact_type = models.CharField(max_length=60)
    schema_version = models.PositiveIntegerField()
    payload = models.JSONField()


class Decision(TenantRow):
    run = models.ForeignKey(AnalysisRun, on_delete=models.PROTECT)
    selected_option = models.CharField(max_length=160)
    reason = models.CharField(max_length=500)
    state = models.CharField(max_length=12, default="draft")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, related_name="+")
    approved_at = models.DateTimeField(null=True)


class Action(Versioned):
    decision = models.ForeignKey(Decision, on_delete=models.PROTECT)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    goal = models.ForeignKey(Goal, null=True, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    planned_cost = models.DecimalField(max_digits=26, decimal_places=8)
    currency = models.CharField(max_length=3)
    status = models.CharField(max_length=12, default="planned")


class Outcome(Versioned):
    action = models.ForeignKey(Action, on_delete=models.PROTECT)
    observation = models.ForeignKey(Observation, on_delete=models.PROTECT)
    interpretation = models.CharField(max_length=500)


class AuditEvent(TenantRow):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    action = models.CharField(max_length=36)
    entity_id = models.UUIDField()


class AuthThrottle(models.Model):
    key = models.CharField(max_length=64, primary_key=True)
    window_end = models.DateTimeField()
    count = models.PositiveIntegerField(default=1)


class IntakePreview(TenantRow):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    kind = models.CharField(max_length=12)
    checksum = models.CharField(max_length=64)
    payload = models.JSONField()
    expires_at = models.DateTimeField()
    applied_id = models.UUIDField(null=True)


class ReportExport(TenantRow):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    source = models.ForeignKey(Dataset, on_delete=models.PROTECT, null=True)
    source_artifact = models.ForeignKey(Artifact, on_delete=models.PROTECT, null=True)
    request_hash = models.CharField(max_length=64)
    format = models.CharField(max_length=4)
    state = models.CharField(max_length=12, default="queued")
    snapshot = models.JSONField()
    result = models.BinaryField(null=True)
    checksum = models.CharField(max_length=64, blank=True, default="")
    renderer_version = models.CharField(max_length=100, blank=True, default="")
    error_code = models.CharField(max_length=32, blank=True, default="")
    expires_at = models.DateTimeField(null=True)
    lease_token = models.UUIDField(null=True)
    lease_until = models.DateTimeField(null=True)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta(TenantRow.Meta):
        constraints = [
            models.UniqueConstraint(fields=["workspace", "request_hash"], name="export_request_once"),
            models.CheckConstraint(
                condition=(Q(source__isnull=False, source_artifact__isnull=True)
                           | Q(source__isnull=True, source_artifact__isnull=False)),
                name="export_exactly_one_source",
            ),
        ]
