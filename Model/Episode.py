from dataclasses import dataclass, field
from datetime import datetime, timezone, date
from typing import List
from dataclasses import fields

@dataclass
class Episode:
    name: str
    air_date: date
    episode: str
    characters: List
    # url: str
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


    @staticmethod
    def getRequiredAttributes():
        return ['name', 'air_date', 'episode']

    @staticmethod
    def getEditableAttributes():
        return ['name', 'air_date', 'episode']
    
    @staticmethod
    def getReferenceAttributes():
        return ['id', 'name', 'episode']

    @staticmethod
    def validateData(data):
        errors = list()
        required = Episode.getRequiredAttributes()
        for field in required:
            if field not in data:
                errors.append(field)
        if errors:
            raise ValueError(f"Missing required values: {str(errors)}")
                
    @staticmethod
    def validateUpdateableValues(data):
        errors = list()
        editables = Episode.getEditableAttributes()

        for key in data:
            if not key in editables:
                errors.append(key)

        if errors:
            raise ValueError(f"Editing fields {str(errors)} is not allowed. Only {str(editables)} allowed")
        

    @staticmethod
    def create(data):
        Episode.validateData(data)
        return Episode(
            name = data['name'],
            air_date = data['air_date'],
            episode = data['episode'],
            characters = data.get('characters', [])
            # url = data.get('url', '')            
        )
    
    @staticmethod
    def getReferenceData(episode):
        fields = Episode.getReferenceAttributes()
        return {field: episode[field] for field in fields}