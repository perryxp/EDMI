from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint

def create_app():
    app = Flask(__name__)

    # inicializa DB y extensiones
    db = init_extensions(app)

    # registra el blueprint pasándole el repo ya configurado
    character_blueprint = create_character_blueprint(db)
    app.register_blueprint(character_blueprint, url_prefix="/api/v1")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
