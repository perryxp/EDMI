from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import List
from dataclasses import fields

@dataclass
class Location:
    name: str
    type: str
    dimension: str
    residents: List[dict] = field(default_factory = list)
    # url: str
    created: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


    @staticmethod
    def getRequiredAttributes():
        return ['name', 'type', 'dimension']

    @staticmethod
    def getEditableAttributes():
        return ['name', 'type', 'dimension']
    
    @staticmethod
    def getReferenceAttributes():
        return ['id', 'name']

    @staticmethod
    def validateData(data):
        errors = list()
        required = Location.getRequiredAttributes()
        for field in required:
            if field not in data:
                errors.append(field)
        if errors:
            raise ValueError(f"Missing required values: {str(errors)}")
                
    @staticmethod
    def validateUpdateableValues(data):
        errors = list()
        editables = Location.getEditableAttributes()

        for key in data:
            if not key in editables:
                errors.append(key)

        if errors:
            raise ValueError(f"Editing fields {str(errors)} is not allowed. Only {str(editables)} allowed")
        

    @staticmethod
    def create(data):
        Location.validateData(data)
        location = Location(
            name = data['name'],
            type = data['type'],
            dimension = data['dimension'],
            residents = data.get('residents', [])
            # url = data.get('url', '')            
        )
        return asdict(location)
    
    @staticmethod
    def getReferenceData(location):
        fields = Location.getReferenceAttributes()
        return {field: location[field] for field in fields}