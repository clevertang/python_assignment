README

## Description

The project is a financial data processing application. It retrieves financial data from a data source, stores it in a
database, and provides an API to query and analyze the data.

## Features

- Retrieve financial data from a data source
- Store financial data in a database
- Provide API endpoints to query financial data
- Perform data analysis and calculations
- Scheduled data retrieval and updates

## Local Installation&Run

1. Clone the repository:

   ```shell
   git clone https://github.com/clevertang/python_assignment.git
   ```

2. Navigate to the project directory:

   ```shell
   cd python_assignment
   ```

3. Install the required dependencies:

   ```shell
   pip install -r requirements.txt
   ```

4. Configure the database connection:

    - Open the `config.py` file and update the `DATABASE_URI` variable with your database connection information.

5. Run the application:

   ```shell
   python app.py
   ```

6. Access the application in your web browser:

   ```
   http://localhost:5005
   ```

## Docker Support

To run the application using Docker, follow these steps:

1. Build the Docker image:

   ```shell
   docker compose buildt .
   ```

2. Run the Docker container:

   ```shell
   docker compose up database
   docker compose up api
   ```

3. Access the application in your web browser:

   ```
   http://localhost:5005
   ```

Please note that you still need to configure the database connection by updating the `DATABASE_URI` variable in
the `config.py` file before running the Docker container.

## Database Configuration

Before starting the application,no matter docker or local, make sure to create the necessary database and tables. For
more details, please refer to the [sql](schema.sql) file.

   ```
   i used the orm but still choose to do ddl,since ddl should be taken by DBA
   ```

## API Documentation

The API provides the following endpoints:

- `/api/financial_data`: Retrieve financial data based on specified filters.
- `/api/statistics`: Perform data analysis and calculate statistics based on specified filters.
- `/start_job`: Start get_raw_data, curl -X POST http://localhost:5005/start_job（only for admin）

For detailed API documentation and usage examples, please refer to the [API Documentation](API_DOCUMENTATION.md) file.

## Libraries and APIs

In this project, the following libraries and APIs are used:

- Flask: A lightweight web framework for building APIs. I use it to build api server
- SQLAlchemy: I use it as ORM，no need to care db session management or sql injection
- APScheduler: I use it to set a crontab task for get_raw_data
- PyMySQL: A Python library for connecting to MySQL databases. I use it in get_raw_data since I need create or update
  operation

## API Key Storage

When it comes to storing API keys securely, there are a few best practices considering:

1. **Database Protection**: Storing API keys in a secure database ensures that only authorized individuals with proper access permissions can retrieve them. By utilizing a gateway or implementing strict access controls, you can restrict database access to authorized personnel only.

2. **Encoding and Encryption**: Encode the API keys using a secure encoding algorithm (e.g., Base64) and encrypt them with a strong encryption key. In the project, you should store only the encoded result of the API keys in the code or somewhere else

3. **Secure Key Management**: Encryption key used to encrypt the API keys should be stored separately in a secure location, such as a key management system or a hardware security module (HSM). This ensures that even if the database is compromised, the encryption key remains secure.

4. **User Password Storage**: When storing user passwords, it is a best practice to store a salted and hashed version of the password instead of the actual password. The salt is a randomly generated value unique to each user, which adds an extra layer of security. When a user attempts to log in, the entered password is hashed with the stored salt value and compared against the stored hashed password.

I can do 2 and 3,but I choose the most easy one. In this case,4 has nothing to do with this case,that's just a practice of my onw experience


## API Test

For detailed API Test, please refer to the [API TEST Documentation](API_TEST.md) file.
