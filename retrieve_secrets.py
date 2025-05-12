import os
import json

def get_and_print_secrets():
    # GitHub Actions automatically exposes secrets as environment variables
    # with the format: SECRETS_NAME
    secret_name = "SF_SECRETS"
    secret_env_var = secret_name
    
    # Try to retrieve the secret from environment variables
    secret_value = os.environ.get(secret_env_var)
    
    if secret_value:
        print(f"Secret {secret_name} retrieved successfully!")
        
        # Check if the secret is JSON formatted
        try:
            # Parse as JSON and print in a formatted way
            secret_json = json.loads(secret_value)
            print("Secret contents (JSON format):")
            print(json.dumps(secret_json, indent=2))
        except json.JSONDecodeError:
            # Print as plain text if not JSON
            print("Secret contents (plain text):")
            print(secret_value)
    else:
        print(f"Error: Secret {secret_name} not found in environment variables.")
        print("Make sure the secret is correctly set in your GitHub repository settings.")

if __name__ == "__main__":
    get_and_print_secrets()