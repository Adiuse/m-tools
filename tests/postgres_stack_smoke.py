"""Check the pinned PostgreSQL runtime with the locked psycopg driver."""

import os
import sys

import psycopg


EXPECTED_SERVER_VERSION = 170012


def main() -> None:
    dsn = os.environ.get("MTOOLS_STACK_POSTGRES_DSN")
    if not dsn:
        print("Set MTOOLS_STACK_POSTGRES_DSN to a development PostgreSQL database.", file=sys.stderr)
        raise SystemExit(2)

    try:
        connection = psycopg.connect(dsn, autocommit=True, connect_timeout=5)
    except (psycopg.OperationalError, psycopg.ProgrammingError):
        print("Could not connect to the configured development PostgreSQL database.", file=sys.stderr)
        raise SystemExit(2) from None

    with connection:
        version = connection.info.server_version
        if version != EXPECTED_SERVER_VERSION:
            print(f"Expected PostgreSQL 17.12 (170012), connected to server version {version}.", file=sys.stderr)
            raise SystemExit(2)

        connection.execute("CREATE TEMP TABLE stack_check (id integer PRIMARY KEY)")
        with connection.transaction():
            connection.execute("INSERT INTO pg_temp.stack_check VALUES (%s)", (1,))

        with connection.transaction(force_rollback=True):
            connection.execute("INSERT INTO pg_temp.stack_check VALUES (%s)", (2,))
            if connection.execute("SELECT count(*) FROM pg_temp.stack_check").fetchone() != (2,):
                raise RuntimeError("The pending insert was not visible inside the transaction.")

        rows = connection.execute("SELECT id FROM pg_temp.stack_check ORDER BY id").fetchall()
        if rows != [(1,)]:
            raise RuntimeError("PostgreSQL did not preserve the committed row and roll back the second insert.")

    print("PASS: PostgreSQL 17.12 connection, commit, and rollback via psycopg.")


if __name__ == "__main__":
    main()
