import os
import json
import snowflake.connector
import subprocess

# Retrieve secrets from environment
secret_name = "SF_SECRETS"
secret_value = os.environ.get(secret_name)
if not secret_value:
    raise RuntimeError(f"Environment variable {secret_name} is missing.")
secrets = json.loads(secret_value)
user, password, account, database, schema, warehouse = (
    secrets['user'], secrets['password'], secrets['account'], secrets['database'], secrets['schema'], secrets['warehouse']
)

# Connect to Snowflake
with snowflake.connector.connect(
    user=user,
    password=password,
    account=account
) as conn:
    with conn.cursor() as cur:
        cur.execute(f'USE DATABASE {database}')
        cur.execute(f'USE SCHEMA {schema}')
        cur.execute(f'USE WAREHOUSE {warehouse}')
        
        # Try to get changed SQL files for both push and PR/MR scenarios
        try:
            # Try to get files changed between origin/main and HEAD (works for PRs/MRs and multi-commit pushes)
            changed_files = subprocess.check_output([
                'git', 'diff', '--name-only', 'origin/main...HEAD'
            ], encoding='utf-8').splitlines()
            print(f"Changed files between origin/main and HEAD: {changed_files}")
            sql_files = [f for f in changed_files if f.startswith('sql/') and f.endswith('.sql')]
            print(f"SQL files to execute: {sql_files}")
        except Exception as e:
            print(f"Error detecting changed SQL files: {e}")
            sql_files = []

        if not sql_files:
            print("No SQL files to execute in this commit or merge request.")

        for sqlfile in sql_files:
            sql_path = os.path.join(os.path.dirname(__file__), sqlfile)
            print(f"Running {sql_path} on Snowflake...")
            with open(sql_path) as f:
                sql = f.read()
            for stmt in sql.split(';'):
                if stmt.strip():
                    print(f"Executing statement: {stmt.strip()[:60]}...")
                    cur.execute(stmt)
