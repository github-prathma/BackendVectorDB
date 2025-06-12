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

1. Library and Chunk Management
- **Create/Read/Update/Delete** Libraries:
Endpoints call LibraryService, which uses LibraryRepository to store and retrieve library data.
- **Create/Read/Update/Delete** Chunks:
Endpoints call LibraryService methods to manage chunks within documents in a library.

2. Embedding with Cohere
- Embedding a Chunk (/libraries/{library_id}/chunks/{chunk_id}/embed/)
   - The endpoint fetches the chunk’s text.
   - Calls **get_cohere_embedding**, which sends the text to Cohere’s API using the API key from .env. Receives the embedding and stores it in the vector database (VectorDB).
   - Receives the embedding and stores it in the vector database (VectorDB).

- Embedding all Chunks (/libraries/{library_id}/embed_all/)
   - Loops through all chunks in all documents of the library.
   - Embeds each chunk using Cohere and stores the embeddings in the vector database.

3. Indexing and Search
- Indexing (/libraries/{library_id}/index/):
   - Accepts a list of embeddings and chunk IDs.
   - Stores them in the vector database for fast retrieval.
- k-NN Search (/libraries/{library_id}/search/)
   - Accepts a query embedding.
   - Uses the selected vector index (brute-force or ball tree) to find the most similar chunks.

## Testing
- Use Swagger UI at http://localhost:8000/docs to interactively test all endpoints.
- test_env.py can be run to verify that .env variables are loaded correctly.

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
