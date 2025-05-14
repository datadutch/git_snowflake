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
        
        # Get only the .sql files changed in the current commit
        try:
            changed_files = subprocess.check_output([
                'git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'
            ], encoding='utf-8').splitlines()
            sql_files = [f for f in changed_files if f.startswith('sql/') and f.endswith('.sql')]
        except Exception as e:
            print(f"Error detecting changed SQL files: {e}")
            sql_files = []

        for sqlfile in sql_files:
            sql_path = os.path.join(os.path.dirname(__file__), sqlfile)
            print(f"Running {sql_path} on Snowflake...")
            with open(sql_path) as f:
                sql = f.read()
            for stmt in sql.split(';'):
                if stmt.strip():
                    cur.execute(stmt)
