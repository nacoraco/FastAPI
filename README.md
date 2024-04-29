# FastAPI Notes App

This is a FastAPI application for managing notes. It provides endpoints for CRUD (Create, Read, Update, Delete) operations on notes stored in an SQLite database.

## Installation

1. Clone the repository:
```git clone https://github.com/nacoraco/FastAPI.git```

4. Navigate to the project directory:
cd FastAPI

5. Install the required dependencies:
pip install -r requirements.txt

6. Run the FastAPI server:
uvicorn main:app --reload

7. Open your web browser and navigate to [http://127.0.0.1:8000/docs#/](http://127.0.0.1:8000/docs#/) to access the Swagger UI. This interactive documentation allows you to explore and test the available API endpoints.

## API Endpoints

- `GET /items/`: Retrieve all notes.
- `GET /items/{item_id}`: Retrieve a specific note by ID.
- `POST /items/`: Create a new note.
- `PUT /items/{item_id}`: Update an existing note.
- `DELETE /items/{item_id}`: Delete an existing note.

## Usage

1. Use the Swagger UI or API endpoints directly to interact with the notes API.
2. Send requests to the appropriate endpoints using tools like cURL, Postman, or your preferred HTTP client.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
