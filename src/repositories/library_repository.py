from src.models.document import Library
from typing import Dict, Optional, List

class LibraryRepository:
    def __init__(self):
        self.libraries: Dict[str, Library] = {}

    def add(self, library: Library):
        self.libraries[library.id] = library

    def get(self, library_id: str) -> Optional[Library]:
        return self.libraries.get(library_id)

    def get_all(self) -> List[Library]:
        return list(self.libraries.values())

    def update(self, library_id: str, library: Library):
        self.libraries[library_id] = library

    def delete(self, library_id: str):
        if library_id in self.libraries:
            del self.libraries[library_id]
