import snowflake.connector
import os
import json

def get_snowflake_secrets():
    try:
        secrets = os.environ['SF_SECRETS']
        print("SF_SECRETS successfully retrieved.")  # Debugging line
        secrets = json.loads(secrets)
        return secrets['user'], secrets['password'], secrets['account'], secrets['database'], secrets['schema'], secrets['warehouse']
    except KeyError as e:
        print(f"Environment variable {str(e)} is missing.")
        raise
    except json.JSONDecodeError:
        print("Failed to decode SF_SECRETS. Ensure it is valid JSON.")
        raise

def create_stage():
    user, password, account, database, schema, warehouse = get_snowflake_secrets()
    with snowflake.connector.connect(
        user=user,
        password=password,
        account=account
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f'USE DATABASE {database}')
            cur.execute(f'USE SCHEMA {schema}')
            cur.execute("CREATE OR REPLACE STAGE st_notebook")

if __name__ == "__main__":
    create_stage()
