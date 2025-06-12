from pydantic import BaseModel
from typing import List, Optional

class Chunk(BaseModel):
    id: str
    content: str
    metadata: Optional[dict] = None

class Document(BaseModel):
    id: str
    title: str
    chunks: List[Chunk]

class Library(BaseModel):
    id: str
    name: str
    documents: List[Document]