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
    try:
        # Retrieve Snowflake credentials
        user, password, account, database, schema, warehouse = get_snowflake_secrets()

        # Connect to Snowflake and create the stage
        with snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        ) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f'USE DATABASE {database}')
                    cur.execute(f'USE SCHEMA {schema}')
                    cur.execute("CREATE OR REPLACE STAGE st_notebook")
                    cur.execute("ALTER STAGE st_notebook SET DIRECTORY = (ENABLE=TRUE, AUTO_REFRESH=FALSE)")  # Corrected syntax for enabling directory table
                    print("Stage 'st_notebook' created successfully with directory table enabled.")
                except Exception as e:
                    print(f"Error while executing Snowflake commands: {e}")
                    raise
    except Exception as e:
        print(f"Error in create_stage: {e}")
        raise

def upload_notebooks_to_stage():
    try:
        # Retrieve Snowflake credentials
        user, password, account, database, schema, warehouse = get_snowflake_secrets()

        # Connect to Snowflake and upload notebooks
        with snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        ) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f'USE DATABASE {database}')
                    cur.execute(f'USE SCHEMA {schema}')

                    # Path to the notebooks directory
                    notebooks_dir = "./notebooks"

                    # Iterate through all files in the notebooks directory
                    for root, _, files in os.walk(notebooks_dir):
                        for file in files:
                            if file.endswith(".ipynb"):
                                file_path = os.path.join(root, file)
                                cur.execute(f"PUT 'file://{file_path}' @st_notebook")
                                print(f"Uploaded {file} to stage 'st_notebook'.")
                except Exception as e:
                    print(f"Error while uploading notebooks: {e}")
                    raise
    except Exception as e:
        print(f"Error in upload_notebooks_to_stage: {e}")
        raise

if __name__ == "__main__":
    try:
        create_stage()
        upload_notebooks_to_stage()
    except Exception as e:
        print(f"Unhandled error: {e}")
