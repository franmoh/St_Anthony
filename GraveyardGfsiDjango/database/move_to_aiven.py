#!/usr/bin/env python3
"""Copy the local cemetery database (MariaDB in Docker) to Aiven for MySQL.

Step 1 - export the local database as a MySQL 8 compatible SQL file:

    python move_to_aiven.py export

Step 2 - load that file into the Aiven service (asks for the password):

    python move_to_aiven.py load --host HOST --port PORT --ca ca.pem

HOST, PORT and ca.pem (the "CA certificate") come from the Aiven service's
Overview page. The export contains the admin login hash and all records, so it
is git-ignored; delete it once the load is done. Needs: pip install pymysql
"""
import argparse
import getpass
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_FILE = HERE / 'cemeterydb_for_aiven.sql'

# MariaDB 11's default collation doesn't exist in MySQL 8; this is its closest equivalent.
COLLATION_MAP = {'utf8mb4_uca1400_ai_ci': 'utf8mb4_0900_ai_ci'}
CHECK_TABLES = ('Section', 'PlotDetails', 'DeceasedDetails', 'Users', 'django_migrations')


def export(container, database, out_path):
    cmd = ['docker', 'exec', container, 'sh', '-c',
           f'exec mariadb-dump -uroot -p"$MARIADB_ROOT_PASSWORD" --single-transaction --skip-comments {database}']
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        sys.exit(f"mariadb-dump failed: {result.stderr.decode(errors='replace').strip()}")
    sql = result.stdout.decode('utf-8')

    # /*M! ... */ lines are MariaDB-only; MySQL would treat each as an empty statement.
    lines = [line for line in sql.splitlines() if not line.startswith('/*M!')]
    sql = '\n'.join(lines) + '\n'
    for old, new in COLLATION_MAP.items():
        sql = sql.replace(old, new)
    leftover = sorted(set(re.findall(r'utf8mb4_uca1400\w*', sql)))
    if leftover:
        sys.exit(f"Unmapped MariaDB collations remain: {leftover}")

    out_path.write_text(sql, encoding='utf-8')
    tables = len(re.findall(r'^CREATE TABLE', sql, flags=re.M))
    print(f"Exported {tables} tables from {container}/{database} -> {out_path} ({out_path.stat().st_size // 1024} KB)")


def statements(sql):
    """Split mariadb-dump output into statements. The dump escapes newlines inside
    values, so every statement ends with ';' at the end of a line."""
    buffer = []
    for line in sql.splitlines():
        if not buffer and (not line.strip() or line.startswith('--')):
            continue
        buffer.append(line)
        if line.rstrip().endswith(';'):
            yield '\n'.join(buffer)
            buffer = []
    if buffer:
        yield '\n'.join(buffer)


def load(sql_path, host, port, user, database, ca, assume_yes):
    try:
        import pymysql
    except ModuleNotFoundError:
        sys.exit("pymysql is required:  pip install pymysql")
    if not sql_path.is_file():
        sys.exit(f"{sql_path} not found - run 'python move_to_aiven.py export' first.")

    password = getpass.getpass(f"Password for {user}@{host}: ")
    ssl = {'ca': str(ca)} if ca else None
    conn = pymysql.connect(host=host, port=port, user=user, password=password, database=database,
                           charset='utf8mb4', ssl=ssl, autocommit=True)
    with conn.cursor() as cur:
        cur.execute('SELECT VERSION()')
        version = cur.fetchone()[0]
        cur.execute("SHOW STATUS LIKE 'Ssl_cipher'")
        cipher = (cur.fetchone() or ('', ''))[1]
        cur.execute('SHOW TABLES')
        existing = [r[0] for r in cur.fetchall()]
    print(f"Connected to {database} on {host}:{port} (MySQL {version}, TLS: {cipher or 'NOT ENCRYPTED'})")

    if existing and not assume_yes:
        answer = input(f"{database} already has {len(existing)} tables; the load replaces those it contains. "
                       "Type 'yes' to continue: ")
        if answer.strip().lower() != 'yes':
            sys.exit("Cancelled.")

    count = 0
    with conn.cursor() as cur:
        for stmt in statements(sql_path.read_text(encoding='utf-8')):
            cur.execute(stmt)
            count += 1
        print(f"Ran {count} statements.")
        for table in CHECK_TABLES:
            cur.execute(f'SELECT COUNT(*) FROM `{table}`')
            print(f"  {table:18} {cur.fetchone()[0]} rows")
    conn.close()
    print("Done. Delete the export file now that it is loaded:", sql_path)


def main():
    parser = argparse.ArgumentParser(description="Move the local cemetery database to Aiven for MySQL.")
    sub = parser.add_subparsers(dest='command', required=True)

    exp = sub.add_parser('export', help="Dump the local Docker database as MySQL 8 compatible SQL.")
    exp.add_argument('--container', default='cemeterydb')
    exp.add_argument('--database', default='cemeterydb')
    exp.add_argument('--out', type=Path, default=DEFAULT_FILE)

    ld = sub.add_parser('load', help="Load the exported SQL into Aiven (or any MySQL server).")
    ld.add_argument('--host', required=True)
    ld.add_argument('--port', type=int, required=True)
    ld.add_argument('--user', default='avnadmin')
    ld.add_argument('--database', default='defaultdb')
    ld.add_argument('--ca', type=Path, help="Aiven CA certificate (ca.pem). Required for Aiven.")
    ld.add_argument('--file', type=Path, default=DEFAULT_FILE)
    ld.add_argument('--yes', action='store_true', help="Don't ask before replacing existing tables.")

    args = parser.parse_args()
    if args.command == 'export':
        export(args.container, args.database, args.out)
    else:
        load(args.file, args.host, args.port, args.user, args.database, args.ca, args.yes)


if __name__ == '__main__':
    main()
