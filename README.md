# Social Networking App Backend

## Introduction

This project aims to provide a robust API for a social networking application using Django Rest Framework.

## Installation

To install and run the Social Networking App Backend locally, follow these steps:

1. Clone the repository:
    ```
    git clone https://github.com/your-username/Social-Networking-App-Backend.git
    ```

2. Navigate to the project directory:
    ```
    cd Social-Networking-App-Backend
    ```

3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

4. Apply migrations:
    ```
    python manage.py migrate
    ```

## Usage

The API will be accessible at `http://localhost:8000/`.

For production use, it's recommended to deploy the application using Docker. Follow these steps:

1. Build the Docker image:
    ```
    docker build -t <img-name> .
    ```

2. Run the Docker container:
    ```
    docker run -d -p 8000:8000 <image-name>
    ```
## Postman Collection

A Postman collection is provided in the root directory of this repository for easy testing of the API endpoints. Import the collection into your Postman application to get started with testing.




