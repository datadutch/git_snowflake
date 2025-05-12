import os
import json
import snowflake.connector

def get_snowflake_secrets():
    # Retrieve secrets from the environment variable
    secret_name = "SF_SECRETS"
    secret_value = os.environ.get(secret_name)

    if not secret_value:
        print(f"Error: Secret {secret_name} not found in environment variables.")
        raise KeyError(f"Environment variable {secret_name} is missing.")

    try:
        # Parse the secret as JSON
        secrets = json.loads(secret_value)
        print("SF_SECRETS successfully retrieved and parsed.")
        return secrets['user'], secrets['password'], secrets['account'], secrets['database'], secrets['schema'], secrets['warehouse']
    except json.JSONDecodeError:
        print("Failed to decode SF_SECRETS. Ensure it is valid JSON.")
        raise

def create_stage():
    # Retrieve Snowflake credentials
    user, password, account, database, schema, warehouse = get_snowflake_secrets()

    # Connect to Snowflake and create the stage
    with snowflake.connector.connect(
        user=user,
        password=password,
        account=account
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f'USE DATABASE {database}')
            cur.execute(f'USE SCHEMA {schema}')
            cur.execute("CREATE OR REPLACE STAGE st_notebook")
            print("Stage 'st_notebook' created successfully.")

if __name__ == "__main__":
    create_stage()
