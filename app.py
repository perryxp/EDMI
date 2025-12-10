from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint
from Repository.CharacterRepository import CharacterRepository
from UseCase.CreateCharacter import CreateCharacter
from UseCase.UpdateCharacter import UpdateCharacter
from UseCase.PartialUpdateCharacter import PartialUpdateCharacter

def create_app():
    app = Flask(__name__)

    # inicializa DB y extensiones
    db = init_extensions(app)

    characterRepository = CharacterRepository(db)

    # casos de uso instanciados aquí
    createCharacter = CreateCharacter(characterRepository)
    updateCharacter = UpdateCharacter(characterRepository)
    partialUpdateCharacter = PartialUpdateCharacter(characterRepository)
    # update_character_uc = UpdateCharacterUseCase(repo)
    # registra el blueprint pasándole el repo ya configurado
    character_controller = create_character_blueprint(
        characterRepository,
        createCharacter,
        updateCharacter,
        partialUpdateCharacter
    )
    app.register_blueprint(character_controller, url_prefix="/api/v1")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
