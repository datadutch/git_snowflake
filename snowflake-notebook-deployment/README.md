# Snowflake Notebook Deployment

This project provides a GitHub Action workflow to deploy Jupyter Notebooks to Snowflake. It includes the necessary configuration files and a sample notebook for demonstration purposes.

## Project Structure

```
snowflake-notebook-deployment
├── .github
│   └── workflows
│       └── deploy-to-snowflake.yml
├── notebooks
│   └── SFBIDUTCH_2025-05-04_20-41-02.ipynb
├── requirements.txt
└── README.md
```

## Getting Started

To get started with deploying your Jupyter Notebook to Snowflake, follow these steps:

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd snowflake-notebook-deployment
   ```

2. **Install Dependencies**
   Make sure to install the required Python packages listed in `requirements.txt`. You can do this using pip:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure GitHub Secrets**
   In your GitHub repository, navigate to `Settings` > `Secrets and variables` > `Actions` and add the following secrets:
   - `SNOWFLAKE_ACCOUNT`: Your Snowflake account name.
   - `SNOWFLAKE_USER`: Your Snowflake username.
   - `SNOWFLAKE_PASSWORD`: Your Snowflake password.
   - `SNOWFLAKE_WAREHOUSE`: The warehouse to use for the deployment.
   - `SNOWFLAKE_DATABASE`: The database to use for the deployment.
   - `SNOWFLAKE_SCHEMA`: The schema to use for the deployment.

4. **Deploy the Notebook**
   Once the secrets are configured, you can push your changes to the main branch. The GitHub Action workflow defined in `.github/workflows/deploy-to-snowflake.yml` will automatically trigger and deploy the notebook to Snowflake.

## Contributing

Feel free to submit issues or pull requests if you have suggestions or improvements for this project.

## License

This project is licensed under the MIT License. See the LICENSE file for details.