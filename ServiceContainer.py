from Repository import (
    CharacterRepository,
    LocationRepository,
    EpisodeRepository
)

from UseCase import (
    CreateCharacter,
    UpdateCharacter,
    PartialUpdateCharacter,
    UpdateCharacterLocation,
    AddCharacterEpisode,
    DeleteCharacterEpisode,
    CharactersPaginator,
)

class ServiceContainer:
    def __init__(self, db):
        self.db = db

        # Mapa de clases para lazy-loading
        self._serviceClasses = {
            # Repositorios
            'characterRepository': lambda: CharacterRepository(self.db),
            'locationRepository': lambda: LocationRepository(self.db),
            'episodeRepository': lambda: EpisodeRepository(self.db),

            # Casos de uso
            'createCharacter': lambda: CreateCharacter(self.get('characterRepository')),
            'updateCharacter': lambda: UpdateCharacter(self.get('characterRepository')),
            'partialUpdateCharacter': lambda: PartialUpdateCharacter(self.get('characterRepository')),
            'updateCharacterLocation': lambda: UpdateCharacterLocation(self.get('characterRepository')),
            'addCharacterEpisode': lambda: AddCharacterEpisode(self.get('characterRepository'), self.get('episodeRepository')),
            'deleteCharacterEpisode': lambda: DeleteCharacterEpisode(self.get('characterRepository'), self.get('episodeRepository')),
            'characterPaginator': lambda: CharactersPaginator(self.get('characterRepository'))
        }

    def get(self, serviceName: str):
        
        if hasattr(self, serviceName):
            return getattr(self, serviceName)

        if serviceName in self._serviceClasses:
            instance = self._serviceClasses[serviceName]()
            setattr(self, serviceName, instance)
            return instance

        raise ValueError(f"Service '{serviceName}' not found in container")
