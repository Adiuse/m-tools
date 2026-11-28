from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("core", "0005_vs02_exports")]
    operations = [
        migrations.RunSQL(
            """
            ALTER TABLE core_intakepreview ADD CONSTRAINT intake_creator_workspace
                FOREIGN KEY (workspace_id, creator_id) REFERENCES core_membership (workspace_id, user_id);
            ALTER TABLE core_reportexport ADD CONSTRAINT report_creator_workspace
                FOREIGN KEY (workspace_id, creator_id) REFERENCES core_membership (workspace_id, user_id);
            ALTER TABLE core_reportexport ADD CONSTRAINT report_source_workspace
                FOREIGN KEY (workspace_id, source_id) REFERENCES core_dataset (workspace_id, id);
            CREATE FUNCTION mtools_export_snapshot() RETURNS trigger LANGUAGE plpgsql AS $$
            BEGIN
                IF OLD.state = 'succeeded' OR
                    ROW(NEW.snapshot, NEW.source_id, NEW.workspace_id, NEW.request_hash, NEW.format)
                    IS DISTINCT FROM ROW(OLD.snapshot, OLD.source_id, OLD.workspace_id, OLD.request_hash, OLD.format)
                THEN
                    RAISE EXCEPTION 'Export snapshots are immutable' USING ERRCODE = 'check_violation';
                END IF;
                RETURN NEW;
            END;
            $$;
            CREATE TRIGGER mtools_export_snapshot BEFORE UPDATE ON core_reportexport
                FOR EACH ROW EXECUTE FUNCTION mtools_export_snapshot();
            """,
            """
            DROP TRIGGER mtools_export_snapshot ON core_reportexport;
            DROP FUNCTION mtools_export_snapshot();
            ALTER TABLE core_reportexport DROP CONSTRAINT report_source_workspace;
            ALTER TABLE core_reportexport DROP CONSTRAINT report_creator_workspace;
            ALTER TABLE core_intakepreview DROP CONSTRAINT intake_creator_workspace;
            """,
        ),
    ]
