from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [("core", "0012_export_renderer_metadata")]
    operations = [
        migrations.RunSQL(
            """
            CREATE FUNCTION mtools_protect_intake_preview() RETURNS trigger LANGUAGE plpgsql AS $$
            BEGIN
                IF OLD.applied_id IS NOT NULL OR NEW.applied_id IS NULL
                    OR (to_jsonb(OLD) - 'payload' - 'applied_id') IS DISTINCT FROM
                       (to_jsonb(NEW) - 'payload' - 'applied_id')
                    OR OLD.payload IS DISTINCT FROM
                       (NEW.payload - 'applied_hash' - 'evidence_id' - 'review_contract') THEN
                    RAISE EXCEPTION 'Intake source and preview are immutable'
                        USING ERRCODE = 'check_violation';
                END IF;
                IF (NEW.kind = 'profile' AND NOT EXISTS (
                    SELECT 1 FROM core_companyprofile WHERE workspace_id = NEW.workspace_id AND id = NEW.applied_id
                )) OR (NEW.kind = 'dataset' AND NOT EXISTS (
                    SELECT 1 FROM core_dataset WHERE workspace_id = NEW.workspace_id AND id = NEW.applied_id
                )) THEN
                    RAISE EXCEPTION 'Intake target must be in the same workspace'
                        USING ERRCODE = 'foreign_key_violation';
                END IF;
                RETURN NEW;
            END;
            $$;
            CREATE TRIGGER mtools_intake_preview BEFORE UPDATE ON core_intakepreview
                FOR EACH ROW EXECUTE FUNCTION mtools_protect_intake_preview();
            """,
            """
            DROP TRIGGER mtools_intake_preview ON core_intakepreview;
            DROP FUNCTION mtools_protect_intake_preview();
            """,
        ),
    ]
