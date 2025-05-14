import os
import json
import snowflake.connector

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
        sql_dir = os.path.join(os.path.dirname(__file__), 'sql')
        for sqlfile in os.listdir(sql_dir):
            if sqlfile.endswith('.sql'):
                sql_path = os.path.join(sql_dir, sqlfile)
                print(f"Running {sql_path} on Snowflake...")
                with open(sql_path) as f:
                    sql = f.read()
                for stmt in sql.split(';'):
                    if stmt.strip():
                        cur.execute(stmt)
