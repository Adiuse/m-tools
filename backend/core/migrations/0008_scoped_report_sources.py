from django.db import migrations


def snapshot_guard(fields):
    return f"""
        CREATE OR REPLACE FUNCTION mtools_export_snapshot() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            IF OLD.state = 'succeeded' OR
                ROW({", ".join("NEW." + field for field in fields)})
                IS DISTINCT FROM ROW({", ".join("OLD." + field for field in fields)})
            THEN
                RAISE EXCEPTION 'Export snapshots are immutable' USING ERRCODE = 'check_violation';
            END IF;
            RETURN NEW;
        END;
        $$;
    """


ORIGINAL = ("snapshot", "source_id", "workspace_id", "request_hash", "format")


class Migration(migrations.Migration):
    dependencies = [("core", "0007_report_sources")]
    operations = [
        migrations.RunSQL(
            "ALTER TABLE core_reportexport ADD CONSTRAINT report_artifact_workspace "
            "FOREIGN KEY (workspace_id, source_artifact_id) REFERENCES core_artifact (workspace_id, id)",
            "ALTER TABLE core_reportexport DROP CONSTRAINT report_artifact_workspace",
        ),
        migrations.RunSQL(snapshot_guard((*ORIGINAL, "source_artifact_id")), snapshot_guard(ORIGINAL)),
    ]
