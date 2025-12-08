from Model import Character

class CharacterService:

    @staticmethod
    def validateData(data):
        for field in Character.requiredAttributes:
            if field not in data:
                raise ValueError(f"Falta el campo obligatorio: {field}")
            
    @staticmethod
    def createCharacter(data):
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
    

