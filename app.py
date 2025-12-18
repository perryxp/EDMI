from flask import Flask
from extensions import init_extensions
from Controller.CharacterController import create_character_blueprint
from Controller.LocationController import create_location_blueprint
from Controller.EpisodeController import create_episode_blueprint
from Controller.AuthController import create_auth_blueprint
from ServiceContainer import ServiceContainer

def create_app():
    app = Flask(__name__)
    app.db = init_extensions(app)

    app.container = ServiceContainer(app.db)
    authController = create_auth_blueprint(app.container)
    characterController = create_character_blueprint(app.container)
    locationController = create_location_blueprint(app.container)
    episodeController = create_episode_blueprint(app.container)
    app.register_blueprint(characterController, url_prefix = '/api/v1')
    app.register_blueprint(locationController, url_prefix = '/api/v1')
    app.register_blueprint(episodeController, url_prefix = '/api/v1')
    app.register_blueprint(authController, url_prefix = '/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
