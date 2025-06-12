# BackendVectorDB
This project is development of REST APIs for indexing and querying documents within a Vector Database. It is built using FastAPI and is designed to handle CRUD operations efficiently.

## Project Structure

```
vector-db-api
├── src
│   ├── main.py                # Entry point of the application
│   ├── api
│   │   └── routes.py          # API endpoints for CRUD operations and embedding
│   ├── db
│   │   └── vector_db.py       # Vector database logic and indexing algorithms
│   ├── models
│   │   └── document.py        # Data models for Chunk, Document, and Library
│   ├── repositories
│   │   └── library_repository.py # Data access layer for libraries
│   └── services
│       ├── library_service.py # Business logic for libraries and chunks
│       └── vector_service.py  # Business logic for vector indexing/search
├── requirements.txt           # Project dependencies
├── Dockerfile                 # Docker image build instructions
├── .dockerignore              # Files to ignore in Docker build
├── test_env.py                # Script to test .env variable loading
└── README.md                  # Project documentation
```

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <parent-folder>
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   uvicorn src.main:app --reload
   ```

## API Usage

The API provides endpoints for managing documents and libraries. You can perform the following operations:

- **Create** a document
- **Read** a document
- **Update** a document
- **Delete** a document

Refer to the API documentation for detailed usage instructions.

## Docker

To build and run the application in a Docker container, use the following commands:

1. Build the Docker image:
   ```
   docker build -t <parent-folder> .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 <parent-folder>
   ```

## Additional Notes

- The project uses Pydantic for data validation and FastAPI for building the API.
- Future enhancements may include adding authentication, more complex querying capabilities, and improved error handling.
