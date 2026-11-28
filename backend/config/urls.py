from django.conf import settings
from django.http import FileResponse, Http404
from django.urls import path
from django.views.decorators.http import require_GET

from core import accounts, analysis, api


@require_GET
def index(request):
    entry = settings.ROOT / "frontend/dist/index.html"
    if not entry.exists():
        raise Http404("Build the frontend or use the Vite development server.")
    return FileResponse(entry.open("rb"), content_type="text/html")


urlpatterns = [
    path("", index),
    path("api/me", accounts.session),
    path("api/auth/login", accounts.sign_in),
    path("api/auth/logout", accounts.sign_out),
    path("api/auth/register", accounts.register),
    path("api/auth/reset", accounts.request_reset),
    path("api/auth/password", accounts.set_password),
    path("api/workspaces", api.workspaces),
    path("api/workspaces/<uuid:workspace_id>/memberships", api.memberships),
    path("api/workspaces/<uuid:workspace_id>/history", api.history),
    path("api/workspaces/<uuid:workspace_id>/datasets", api.entities, {"kind": "datasets"}),
    path("api/workspaces/<uuid:workspace_id>/actions", api.entities, {"kind": "actions"}),
    path("api/workspaces/<uuid:workspace_id>/outcomes", api.entities, {"kind": "outcomes"}),
    path("api/workspaces/<uuid:workspace_id>/entities/<str:kind>", api.entities),
    path("api/workspaces/<uuid:workspace_id>/entities/<str:kind>/<uuid:pk>", api.entity),
    path("api/tools", analysis.tools),
    path("api/tools/<str:tool_id>", analysis.tools),
    path("api/scratch", analysis.scratch),
    path("api/workspaces/<uuid:workspace_id>/preflight", analysis.preflight),
    path("api/workspaces/<uuid:workspace_id>/drafts", analysis.drafts),
    path("api/workspaces/<uuid:workspace_id>/drafts/<uuid:pk>", analysis.drafts),
    path("api/workspaces/<uuid:workspace_id>/runs", analysis.runs),
    path("api/workspaces/<uuid:workspace_id>/runs/<uuid:pk>", analysis.runs),
    path("api/workspaces/<uuid:workspace_id>/artifacts/<uuid:pk>", analysis.artifact),
    path("api/workspaces/<uuid:workspace_id>/artifacts/<uuid:pk>/download", analysis.artifact, {"download": True}),
    path("api/workspaces/<uuid:workspace_id>/runs/<uuid:pk>/sources", analysis.sources),
    path("api/workspaces/<uuid:workspace_id>/decisions", analysis.decisions),
    path("api/workspaces/<uuid:workspace_id>/decisions/<uuid:pk>/approve", analysis.approve),
]
