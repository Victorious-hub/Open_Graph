# Project Information
The project is an API for storing user links. It allows users to register with an email and password, change their password, reset their password, authenticate themselves, and manage their links (create, edit, delete, view). Users can also manage their collections (create, edit, delete, view). Created by Victor Shyshko


### Launching the Project

To launch the project, follow these steps:

1. Make sure you have Docker and Docker Compose installed on your machine.

2. Clone the repository to your local machine:

    ```bash
    git clone https://github.com/Victorious-hub/Open_Graph.git
    ```

3. Navigate to the manage.py file:


4. Create a `.env` file in the project directory and configure the necessary environment variables. Here's an example of the `.env` file:

    ```plaintext
    DB_HOST=db
    DB_PORT=5432
    DB_NAME=mydatabase
    DB_USER=myuser
    DB_PASSWORD=mypassword
    ```

    Replace the values with your own database configuration.

5. Build and start the project using Docker Compose:

    ```bash
    make docker-dev-build
    ```

    This command will build the Docker images and start the containers.

6. Make migrations

    ```bash
    make migrate
    ```

6. Once the containers are up and running, you can access the API at `http://0.0.0.0:8000/api/schema/swagger-ui/`.

    You can use tools like cURL or Postman to interact with the API endpoints.

### All users have password "string". Only user with email "s@gmail.com" has password "1"

