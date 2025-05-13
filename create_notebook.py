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

def get_notebook_name_from_commit():
    # Try to get the notebook name from the latest git commit (including added/modified files)
    try:
        import subprocess
        # Get the list of files changed in the last commit
        files = subprocess.check_output(['git', 'diff-tree', '--no-commit-id', '--name-only', '-r', 'HEAD'], encoding='utf-8').splitlines()
        for file in files:
            if file.endswith('.ipynb'):
                notebook_name = os.path.splitext(os.path.basename(file))[0]
                print(f"Notebook name from commit: {notebook_name}")
                return notebook_name
        # Fallback: try commit message as before
        commit_msg = subprocess.check_output(['git', 'log', '-1', '--pretty=%B'], encoding='utf-8').strip()
        import re
        match = re.search(r'([\w\- ]+\.ipynb)', commit_msg)
        if match:
            notebook_file = match.group(1)
            notebook_name = notebook_file.replace('.ipynb', '')
            print(f"Notebook name from commit message: {notebook_name}")
            return notebook_name
        print("No notebook name found in commit files or message. Using default.")
        return os.environ.get('NOTEBOOK_NAME', 'MyFirstNoteBook')
    except Exception as e:
        print(f"Error extracting notebook name from commit: {e}")
        return os.environ.get('NOTEBOOK_NAME', 'MyFirstNoteBook')

def create_notebook_from_stage():
    try:
        user, password, account, database, schema, warehouse = get_snowflake_secrets()
        notebook_name = get_notebook_name_from_commit()
        main_file = f"{notebook_name}.ipynb"
        branch = os.environ.get('GIT_BRANCH', 'main')
        runtime_name = os.environ.get('RUNTIME_NAME', 'SYSTEM$WAREHOUSE_RUNTIME')
        query_warehouse = os.environ.get('QUERY_WAREHOUSE', 'W_DEV')
        warehouse_name = os.environ.get('WAREHOUSE_NAME', 'SYSTEM$STREAMLIT_NOTEBOOK_WH')
        stage_name = os.environ.get('STAGE_NAME', 'GIT_SNOWFLAKE')

        with snowflake.connector.connect(
            user=user,
            password=password,
            account=account
        ) as conn:
            with conn.cursor() as cur:
                try:
                    cur.execute(f'USE DATABASE {database}')
                    cur.execute(f'USE SCHEMA {schema}')
                    cur.execute(f'USE WAREHOUSE {warehouse}')
                    # Compose the full identifier and path (no IDENTIFIER() wrapper)
                    notebook_identifier = f'"{database}"."{schema}"."{notebook_name}"'
                    stage_path = f'@"{database}"."{schema}"."{stage_name}"/branches/"{branch}"/{notebook_name}/'
                    sql = f"""
                        CREATE NOTEBOOK {notebook_identifier}
                        FROM '{stage_path}'
                        WAREHOUSE = '{warehouse_name}'
                        QUERY_WAREHOUSE = '{query_warehouse}'
                        RUNTIME_NAME = '{runtime_name}'
                        MAIN_FILE = '{main_file}'
                    """
                    cur.execute(sql)
                    print(f"Notebook {notebook_name} created successfully from stage.")
                except Exception as e:
                    print(f"Error while creating notebook: {e}")
                    raise
    except Exception as e:
        print(f"Error in create_notebook_from_stage: {e}")
        raise

if __name__ == "__main__":
    try:
        create_notebook_from_stage()
    except Exception as e:
        print(f"Unhandled error: {e}")
