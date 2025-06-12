from src.models.document import Library, Chunk
from typing import List

class LibraryService:
    def __init__(self, library_repository):
        self.library_repository = library_repository

    def create_library(self, library: Library):
        if self.library_repository.get(library.id):
            raise ValueError("Library already exists")
        self.library_repository.add(library)
        return library

    def get_library(self, library_id: str):
        library = self.library_repository.get(library_id)
        if not library:
            raise ValueError("Library not found")
        return library

    def get_libraries(self):
        return self.library_repository.get_all()

    def update_library(self, library_id: str, library: Library):
        if not self.library_repository.get(library_id):
            raise ValueError("Library not found")
        self.library_repository.update(library_id, library)
        return library

    def delete_library(self, library_id: str):
        if not self.library_repository.get(library_id):
            raise ValueError("Library not found")
        self.library_repository.delete(library_id)

    def add_chunk(self, library_id: str, chunk: Chunk):
        library = self.get_library(library_id)
        if not library.documents:
            raise ValueError("No documents in library")
        library.documents[0].chunks.append(chunk)
        self.library_repository.update(library_id, library)
        return chunk

    def get_chunk(self, library_id: str, chunk_id: str):
        library = self.get_library(library_id)
        for doc in library.documents:
            for chunk in doc.chunks:
                if chunk.id == chunk_id:
                    return chunk
        raise ValueError("Chunk not found")

    def update_chunk(self, library_id: str, chunk_id: str, chunk: Chunk):
        library = self.get_library(library_id)
        for doc in library.documents:
            for i, c in enumerate(doc.chunks):
                if c.id == chunk_id:
                    doc.chunks[i] = chunk
                    self.library_repository.update(library_id, library)
                    return chunk
        raise ValueError("Chunk not found")

    def delete_chunk(self, library_id: str, chunk_id: str):
        library = self.get_library(library_id)
        for doc in library.documents:
            for i, chunk in enumerate(doc.chunks):
                if chunk.id == chunk_id:
                    del doc.chunks[i]
                    self.library_repository.update(library_id, library)
                    return
        raise ValueError("Chunk not found")
