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

