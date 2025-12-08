from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


requiredAttributes = ['name', 'status', 'species', 'gender']

@dataclass
class Character:
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    origin_name: str
    location_name: str
    episode_ids: List[int] = field(default_factory=list)
    image: str = ""
    created_at: datetime = field(default_factory=datetime.now(timezone.utc))
    rating: float = 0.0
    created_by_user: bool = True

