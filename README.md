# FastAPI Notes App

This is a FastAPI application for managing notes. It provides endpoints for CRUD (Create, Read, Update, Delete) operations on notes stored in an SQLite database.

## Installation
1. Install git:
```sudo apt install git```

2. Clone the repository:
```git clone https://github.com/nacoraco/FastAPI.git```

3. Navigate to the project directory:
```cd FastAPI```

4. Install python:
```sudo apt install python3.12-venv```

5. Create a virtual environment named "fastapi":
```python3 -m venv fastapi```

6. Activate the virtual environment:
```source fastapi/bin/activate```

7. Install the required dependencies:
```pip install -r requirements.txt```

8. Run the FastAPI server:
```uvicorn main:app --reload```

9. Open your web browser and navigate to [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/) to access the Swagger UI. This interactive documentation allows you to explore and test the available API endpoints.

10. Open your web browser and navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to access notes app UI.

## Usage

1. Use the Swagger UI or API endpoints directly to interact with the notes API.
2. Send requests to the appropriate endpoints using tools like cURL, Postman, or your preferred HTTP client.
3. Use notes app directly with UI.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
