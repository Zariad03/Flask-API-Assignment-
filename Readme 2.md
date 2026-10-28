
# Flask JSON API Assignment

**Author:** Zaria

## Description

This project contains a Flask API with two endpoints. The API returns JSON responses and validates input before processing requests.

## Requirements

- Python 3
- Flask
- pytest for automated testing

## Install Dependencies

Run the following command:

    python -m pip install -r requirements.txt

## Run the Application

Run the following command:

    python app.py

The application runs on port 5000.

## Endpoint 1: GET /hello

Returns a greeting using the default name or a custom name.

**Example URL:**

    http://127.0.0.1:5000/hello

**Expected response:**

    {"message": "Hello, Zaria!"}

**Custom name example:**

    http://127.0.0.1:5000/hello?name=John

**Expected response:**

    {"message": "Hello, John!"}

## Endpoint 2: POST /sum

Accepts a JSON object containing a list of numbers and returns their sum.

**Example request:**

    {"numbers": [1, 2, 3]}

**Expected response:**

    {"sum": 6}

Invalid input returns HTTP 400. An unsupported HTTP method returns HTTP 405.

## Run Automated Tests

Make sure app.py and test_app.py are in the same project folder.

Run the tests using:

    python -m unittest -v test_app

The tests cover greetings, whole numbers, decimal numbers, negative numbers, empty lists, invalid JSON, missing data, incorrect data types, and unsupported HTTP methods.

## Project Files

- app.py: Flask application
- test_app.py: Automated tests
- requirements.txt: Required Python packages
- README.md: Setup and usage instructions
- .gitignore: Excludes temporary files
