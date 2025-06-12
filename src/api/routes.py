from fastapi import APIRouter, HTTPException, Body, Depends
from src.models.document import Library, Chunk
from typing import List
from src.repositories.library_repository import LibraryRepository
from src.services.library_service import LibraryService
from src.db.vector_db import VectorDB
from src.services.vector_service import VectorService

router = APIRouter()

# Dependency providers
library_repository = LibraryRepository()
library_service = LibraryService(library_repository)
vector_db = VectorDB()
vector_service = VectorService(vector_db)

# Library CRUD
@router.post("/libraries/", response_model=Library)
async def create_library(library: Library):
    try:
        return library_service.create_library(library)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/libraries/", response_model=List[Library])
async def read_libraries():
    return library_service.get_libraries()

@router.get("/libraries/{library_id}", response_model=Library)
async def read_library(library_id: str):
    try:
        return library_service.get_library(library_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/libraries/{library_id}", response_model=Library)
async def update_library(library_id: str, library: Library):
    try:
        return library_service.update_library(library_id, library)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/libraries/{library_id}")
async def delete_library(library_id: str):
    try:
        library_service.delete_library(library_id)
        return {"detail": "Library deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Chunk CRUD within a library
@router.post("/libraries/{library_id}/chunks/", response_model=Chunk)
async def create_chunk(library_id: str, chunk: Chunk):
    try:
        return library_service.add_chunk(library_id, chunk)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/libraries/{library_id}/chunks/{chunk_id}", response_model=Chunk)
async def read_chunk(library_id: str, chunk_id: str):
    try:
        return library_service.get_chunk(library_id, chunk_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.put("/libraries/{library_id}/chunks/{chunk_id}", response_model=Chunk)
async def update_chunk(library_id: str, chunk_id: str, chunk: Chunk):
    try:
        return library_service.update_chunk(library_id, chunk_id, chunk)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/libraries/{library_id}/chunks/{chunk_id}")
async def delete_chunk(library_id: str, chunk_id: str):
    try:
        library_service.delete_chunk(library_id, chunk_id)
        return {"detail": "Chunk deleted"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

# Indexing endpoint (expects embedding for each chunk)
@router.post("/libraries/{library_id}/index/")
async def index_library(library_id: str, embeddings: List[List[float]] = Body(...)):
    try:
        library = library_service.get_library(library_id)
        if not library.documents:
            raise ValueError("No documents in library")
        doc = library.documents[0]
        chunk_ids = [chunk.id for chunk in doc.chunks]
        vector_service.index_chunks(chunk_ids, embeddings)
        return {"detail": "Library indexed"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# k-NN search endpoint
@router.post("/libraries/{library_id}/search/")
async def search_library(library_id: str, query_embedding: List[float] = Body(...), top_k: int = 5):
    try:
        library = library_service.get_library(library_id)
        if not library.documents:
            raise ValueError("No documents in library")
        results = vector_service.search(query_embedding, top_k=top_k)
        return {"chunk_ids": results}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


def get_cohere_embedding(text: str) -> List[float]:
    import os
    import requests
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    if not COHERE_API_KEY:
        raise RuntimeError("COHERE_API_KEY is not set. Please check your .env file and environment variables.")
    url = "https://api.cohere.ai/v1/embed"
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "texts": [text],
        "model": "embed-english-v3.0"
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()["embeddings"][0]

@router.post("/libraries/{library_id}/chunks/{chunk_id}/embed/")
async def embed_chunk(library_id: str, chunk_id: str):
    try:
        chunk = library_service.get_chunk(library_id, chunk_id)
        embedding = get_cohere_embedding(chunk.content)
        vector_db.index_document(chunk.id, embedding)
        return {"embedding": embedding}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/libraries/{library_id}/embed_all/")
async def embed_all_chunks(library_id: str):
    try:
        library = library_service.get_library(library_id)
        results = []
        for doc in library.documents:
            for chunk in doc.chunks:
                embedding = get_cohere_embedding(chunk.content)
                vector_db.index_document(chunk.id, embedding)
                results.append({"chunk_id": chunk.id, "embedding": embedding})
        return {"embeddings": results}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))