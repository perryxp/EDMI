from Model.Character import Character
from pprint import pprint
class CharacterService:

    @staticmethod
    def validateData(data):
        for field in Character.getRequiredAttributes():
            if field not in data:
                raise ValueError(f"Falta el campo obligatorio: {field}")
            
    @staticmethod
    def createCharacter(data):
        CharacterService.validateData(data)
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
    
    @staticmethod
    def validateUpdateableValues(data):
        errors = list()
        editables = Character.getEditableAttributes()

        for key in data:
            if not key in editables:
                errors.append(key)

            if errors:
                raise ValueError(f"Editing fields " + str(errors) + " is not allowed. Only " + str(editables) + " allowed")
    

