from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint
from Repository.CharacterRepository import CharacterRepository
from Repository.LocationRepository import LocationRepository
from Repository.EpisodeRepository import EpisodeRepository
from UseCase.CreateCharacter import CreateCharacter
from UseCase.UpdateCharacter import UpdateCharacter
from UseCase.PartialUpdateCharacter import PartialUpdateCharacter
from UseCase.UpdateCharacterLocation import UpdateCharacterLocation
from UseCase.AddCharacterEpisode import AddCharacterEpisode
from UseCase.DeleteCharacterEpisode import DeleteCharacterEpisode

def create_app():
    app = Flask(__name__)

    # inicializa DB y extensiones
    db = init_extensions(app)

    # instanciar repositorios
    characterRepository = CharacterRepository(db)
    locationRepository = LocationRepository(db)
    episodeRepository = EpisodeRepository(db)
    # casos de uso instanciados aquí
    createCharacter = CreateCharacter(characterRepository)
    updateCharacter = UpdateCharacter(characterRepository)
    partialUpdateCharacter = PartialUpdateCharacter(characterRepository)
    updateCharacterLocation = UpdateCharacterLocation(characterRepository)
    addCharacterEpisode = AddCharacterEpisode(characterRepository, episodeRepository)
    deleteCharacterEpisode = DeleteCharacterEpisode(characterRepository, episodeRepository)
    # update_character_uc = UpdateCharacterUseCase(repo)
    # registra el blueprint pasándole el repo ya configurado
    character_controller = create_character_blueprint(
        characterRepository,
        createCharacter,
        updateCharacter,
        partialUpdateCharacter,
        locationRepository,
        updateCharacterLocation,
        addCharacterEpisode,
        episodeRepository,
        deleteCharacterEpisode
    )
    app.register_blueprint(character_controller, url_prefix="/api/v1")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
