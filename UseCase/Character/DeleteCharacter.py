from Exception.NotFoundException import NotFoundException
from Exception.ConflictException import ConflictException
from pprint import pprint

class DeleteCharacter:
    characterRepo = None
    locationRepo = None
    dbManager = None

    def __init__(self, characterRepo, locationRepo, dbManager):
        self.characterRepo = characterRepo
        self.locationRepo = locationRepo
        self.dbManager = dbManager

    def do(self, characterId):
        character = self.characterRepo.findOne(characterId)
        if not character:
            raise NotFoundException()
        
        if 'episodes' in character and len(character['episodes']) > 0:
            raise ConflictException(f'Character "{character['name']}" exists in episodes {str(character['episodes'])}')
        
        with self.dbManager.transaction() as session:
            if 'location' in character and 'id' in character['location']:
                self.__deleteResidentFromLocation(character, session)
            self.characterRepo.deleteCharacter(character['id'], session)
                

    def __deleteResidentFromLocation(self, resident, session):    
        location = self.locationRepo.findOne(['location']['id'])        
        for i, residentInfo in enumerate(location['residents']):
            if residentInfo['id'] == resident['id']:
                del location['residents'][i]
                break
        return self.locationRepo.updateLocation(location['id'], location, session)
    