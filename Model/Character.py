from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List
from dataclasses import fields


@dataclass
class Character:
    # id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin_name: str
    location_name: str
    episode_ids: List[int] = field(default_factory=list)
    image: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    rating: float = 0.0
    created_by_user: bool = True

    @staticmethod
    def getRequiredAttributes():
        return ['name', 'status', 'species', 'gender']

    @staticmethod
    def getEditableAttributes():
        return ['name', 'status', 'species', 'gender', 'image', 'rating']

    @staticmethod
    def validateData(data):
        for field in Character.getRequiredAttributes():
            if field not in data:
                raise ValueError(f"Falta el campo obligatorio: {field}")
            
    @staticmethod
    def validateUpdateableValues(data):
        errors = list()
        editables = Character.getEditableAttributes()

        for key in data:
            if not key in editables:
                errors.append(key)

            if errors:
                raise ValueError(f"Editing fields " + str(errors) + " is not allowed. Only " + str(editables) + " allowed")
    
    
    @staticmethod
    def create(data):
        Character.validateData(data)
        return Character(
            # id = data["id"],
            name = data["name"],
            status = data.get("status", "unknown"),
            species = data.get("species", ""),
            type = data.get("type", ""),
            gender = data.get("gender", ""),
            origin_name = data.get("origin", {}).get("name", ""),
            location_name = data.get("location", {}).get("name", ""),
            # episode_ids = _extract_episode_ids(data.get("episode", [])),
            # image = data.get("image", "")
        )