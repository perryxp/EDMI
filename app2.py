from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint
from Controller.LocationController import create_location_blueprint
from ServiceContainer import ServiceContainer

def create_app():
    app = Flask(__name__)
    db = init_extensions(app)

    container = ServiceContainer(db)
    characterController = create_character_blueprint(container)
    locationController = create_location_blueprint(container)
    app.register_blueprint(characterController, url_prefix= '/api/v1')
    app.register_blueprint(locationController, url_prefix= '/api/v1')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
