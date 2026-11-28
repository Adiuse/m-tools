from django.db import migrations


# A regular ORM FK checks existence; this composite FK also checks ownership.
RELATIONS = (
    ("dataset", "evidence", "evidence"),
    ("observation", "metric", "metricdefinition"),
    ("observation", "dataset", "dataset"),
    ("observation", "evidence", "evidence"),
    ("goal", "metric", "metricdefinition"),
    ("goal", "baseline", "observation"),
    ("hypothesis", "evidence", "evidence"),
    ("job", "run", "analysisrun"),
    ("artifact", "run", "analysisrun"),
    ("decision", "run", "analysisrun"),
    ("action", "decision", "decision"),
    ("action", "goal", "goal"),
    ("outcome", "action", "action"),
    ("outcome", "observation", "observation"),
)
MEMBER_REFERENCES = (
    ("goal", "owner"), ("action", "owner"), ("evidence", "created_by"),
    ("dataset", "created_by"), ("analysisrun", "creator"), ("rundraft", "creator"),
    ("decision", "created_by"), ("decision", "approved_by"), ("auditevent", "actor"),
)
IMMUTABLE_TABLES = (
    "companyprofile", "evidence", "dataset", "metricdefinition", "observation", "goal",
    "hypothesis", "action", "outcome", "artifact", "rundraft", "auditevent",
)


def compound_fk(table, field, parent, parent_key):
    name = f"{table}_{field}_same_workspace"
    return migrations.RunSQL(
        f"ALTER TABLE core_{table} ADD CONSTRAINT {name} "
        f"FOREIGN KEY (workspace_id, {field}_id) REFERENCES core_{parent} "
        f"(workspace_id, {parent_key}) DEFERRABLE INITIALLY IMMEDIATE",
        f"ALTER TABLE core_{table} DROP CONSTRAINT {name}",
    )


class Migration(migrations.Migration):
    dependencies = [("core", "0001_initial")]
    operations = [
        *(compound_fk(table, field, parent, "id") for table, field, parent in RELATIONS),
        *(compound_fk(table, field, "membership", "user_id") for table, field in MEMBER_REFERENCES),
        migrations.RunSQL(
            """
            CREATE FUNCTION mtools_immutable_record() RETURNS trigger LANGUAGE plpgsql AS $$
            BEGIN
                RAISE EXCEPTION 'Create a new version instead of editing an existing record'
                    USING ERRCODE = 'check_violation';
            END;
            $$;
            """,
            "DROP FUNCTION mtools_immutable_record()",
        ),
        *(
            migrations.RunSQL(
                f"CREATE TRIGGER mtools_immutable BEFORE UPDATE ON core_{table} "
                "FOR EACH ROW EXECUTE FUNCTION mtools_immutable_record()",
                f"DROP TRIGGER mtools_immutable ON core_{table}",
            )
            for table in IMMUTABLE_TABLES
        ),
        migrations.RunSQL(
            """
            CREATE FUNCTION mtools_protect_run() RETURNS trigger LANGUAGE plpgsql AS $$
            BEGIN
                IF OLD.status IN ('succeeded', 'failed')
                    OR (to_jsonb(OLD) - 'status' - 'result') IS DISTINCT FROM
                       (to_jsonb(NEW) - 'status' - 'result') THEN
                    RAISE EXCEPTION 'Run snapshots and terminal runs are immutable'
                        USING ERRCODE = 'check_violation';
                END IF;
                RETURN NEW;
            END;
            $$;
            CREATE TRIGGER mtools_run_snapshot BEFORE UPDATE ON core_analysisrun
                FOR EACH ROW EXECUTE FUNCTION mtools_protect_run();
            """,
            """
            DROP TRIGGER mtools_run_snapshot ON core_analysisrun;
            DROP FUNCTION mtools_protect_run();
            """,
        ),
    ]
