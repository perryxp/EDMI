from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List
from dataclasses import fields


@dataclass
class Character:
    name: str
    status: str
    species: str
    character_type: str
    gender: str
    origin: dict
    location: dict
    episodes: List[dict] = field(default_factory = list)
    image: str = ''
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_by_user: bool = True

    @staticmethod
    def getRequiredAttributes():
        return ['name', 'status', 'species', 'gender']

    @staticmethod
    def getEditableAttributes():
        return ['name', 'status', 'species', 'gender', 'image']
    
    @staticmethod
    def getReferenceAttributes():
        return ['id', 'name']

    @staticmethod
    def validateData(data):
        errors = list()
        required = Character.getRequiredAttributes()
        for field in required:
            if field not in data:
                errors.append(field)
        if errors:
            raise ValueError(f'Missing required values: {str(errors)}')
            
    @staticmethod
    def validateUpdateableValues(data):
        errors = list()
        editables = Character.getEditableAttributes()

        for key in data:
            if not key in editables:
                errors.append(key)

        if errors:
            raise ValueError(f'Editing fields {str(errors)} is not allowed. Only {str(editables)} allowed')
    

    @staticmethod
    def create(data):
        Character.validateData(data)
        character = Character(
            name = data['name'],
            status = data.get('status', 'unknown'),
            species = data.get('species', 'unknown'),
            character_type = data.get('character_type', 'unknown'),
            gender = data.get('gender', 'unknown'),
            origin = data.get('origin', 'unknown'),
            location = data.get('location', 'unknown'),
            episodes = data.get('episodes', []),
            image = data.get('image', '')
        )

        return asdict(character)
    
    
    @staticmethod
    def getReferenceData(character):
        fields = Character.getReferenceAttributes()
        return {field: character[field] for field in fields}

        