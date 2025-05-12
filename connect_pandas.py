# https://docs.snowflake.com/en/user-guide/python-connector.html

import snowflake.connector
import json
import pandas as pd
import os

# Function to get Snowflake secrets from the SF_SECRETS environment variable
def get_snowflake_secrets():
    secrets = json.loads(os.environ['SF_SECRETS'])
    return secrets['user'], secrets['password'], secrets['account']

# Retrieve secrets
user, password, account = get_snowflake_secrets()

# Connect to Snowflake
con = snowflake.connector.connect(
    user=user,
    password=password,
    account=account
)

con.cursor().execute("USE WAREHOUSE W_DEV;")

query_inf = "SELECT * FROM D_DEV.INFORMATION_SCHEMA.TABLES;"

# Execute query and load into Pandas DataFrame
df = pd.read_sql_query(query_inf, con)
print(df)