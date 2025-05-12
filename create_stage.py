import snowflake.connector
import os

def create_stage():
    with snowflake.connector.connect(
        user=os.environ['SNOWFLAKE_USER'],
        password=os.environ['SNOWFLAKE_PASSWORD'],
        account=os.environ['SNOWFLAKE_ACCOUNT']
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f'USE DATABASE {os.environ["SNOWFLAKE_DATABASE"]}')
            cur.execute(f'USE SCHEMA {os.environ["SNOWFLAKE_SCHEMA"]}')
            cur.execute("CREATE OR REPLACE STAGE st_notebook")

if __name__ == "__main__":
    create_stage()
