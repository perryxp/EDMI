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
    CharactersPaginator,
    LocationsPaginator,
    CreateLocation,
    UpdateLocation,
    PartialUpdateLocation,
    DeleteLocation,
    EpisodesPaginator,
    CreateEpisode,
    UpdateEpisode,
    PartialUpdateEpisode,
    DeleteEpisode,
    AddEpisodeCharacter,
    AddEpisodeLocation,
    DeleteEpisodeLocation,
    DeleteEpisodeCharacter,
    DeleteCharacter,
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
            'createCharacter': lambda: CreateCharacter(
                self.get('characterRepository'),
                self.get('locationRepository')
            ),
            'updateCharacter': lambda: UpdateCharacter(
                self.get('characterRepository'),
                self.get('locationRepository'),
            ),
            'partialUpdateCharacter': lambda: PartialUpdateCharacter(self.get('characterRepository')),
            'updateCharacterLocation': lambda: UpdateCharacterLocation(
                self.get('characterRepository'),
                self.get('locationRepository')
            ),
            'deleteCharacter': lambda: DeleteCharacter(
                self.get('characterRepository'),
                self.get('locationRepository'),
                self.db,
            ),
            'characterPaginator': lambda: CharactersPaginator(self.get('characterRepository')),
            'locationsPaginator': lambda: LocationsPaginator(self.get('locationRepository')),
            'createLocation': lambda: CreateLocation(self.get('locationRepository')),
            'updateLocation': lambda: UpdateLocation(self.get('locationRepository')),
            'partialUpdateLocation': lambda: PartialUpdateLocation(self.get('locationRepository')),
            'deleteLocation': lambda: DeleteLocation(self.get('locationRepository')),
            'episodesPaginator': lambda: EpisodesPaginator(self.get('episodeRepository')),
            'createEpisode': lambda: CreateEpisode(self.get('episodeRepository')),
            'updateEpisode': lambda: UpdateEpisode(self.get('episodeRepository')),
            'partialUpdateEpisode': lambda: PartialUpdateEpisode(self.get('episodeRepository')),
            'deleteEpisode': lambda: DeleteEpisode(self.get('episodeRepository')),
            'addEpisodeLocation': lambda: AddEpisodeLocation(
                self.get('episodeRepository'),
                self.get('locationRepository'),
            ),
            'deleteEpisodeLocation': lambda: DeleteEpisodeLocation(
                self.get('episodeRepository'),
                self.get('locationRepository'),
            ),
            'addEpisodeCharacter': lambda: AddEpisodeCharacter(
                self.get('episodeRepository'),
                self.get('characterRepository'),
            ),
            'deleteEpisodeCharacter': lambda: DeleteEpisodeCharacter(
                self.get('episodeRepository'),
                self.get('characterRepository')
            ),
        }

    def get(self, serviceName: str):
        
        if hasattr(self, serviceName):
            return getattr(self, serviceName)

        if serviceName in self._serviceClasses:
            instance = self._serviceClasses[serviceName]()
            setattr(self, serviceName, instance)
            return instance

        raise ValueError(f"Service '{serviceName}' not found in container")
