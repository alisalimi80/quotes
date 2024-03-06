# Qoute third-party project

This repository contains a Django project for get and show quotes from third-party pakage.

## Prerequisites

Before getting started, ensure you have the following installed on your system:

- Docker: [Installation Guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation Guide](https://docs.docker.com/compose/install/)

## Getting Started

1. Clone the repository:
2. Navigate to the project directory:
3. Build the Docker containers:

    ```bash
    docker-compose build
    ```

4. Run the Docker containers:

    ```bash
    docker-compose up
    ```

5. Access the Django application:

    Open a web browser and go to `http://localhost:8001` and api document with swagger in `http://localhost:8001/api/schema/swagger-ui/#/`

## Development

- The Django project code is located in the `quotes/` directory.
- Make changes to the Django application code as needed. The server will automatically reload with any changes you make.
- Access the Django admin panel at `http://localhost:8001/admin/` with the default admin credentials (username: `admin`, password: `12345678910`).

## Docker Compose Commands

- Start the containers: `docker-compose up`
- Stop the containers: `docker-compose down`
- Rebuild the containers: `docker-compose build`
- View logs: `docker-compose logs`
