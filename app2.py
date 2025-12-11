from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint
from ServiceContainer import ServiceContainer

def create_app():
    app = Flask(__name__)
    db = init_extensions(app)

    container = ServiceContainer(db)
    character_controller = create_character_blueprint(container)
    app.register_blueprint(character_controller, url_prefix="/api/v1")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
