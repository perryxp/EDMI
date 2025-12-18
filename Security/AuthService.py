from werkzeug.exceptions import NotFound
import secrets
from pprint import pprint

class AuthService:
    userRepo = None
    apikeyRepo = None
    _APIKEY_LIFETIME = 3600 # segundos
    _APIKEY_LENGTH = 32

    def __init__(self, userRepo, apikeyRepo):        
        self.userRepo = userRepo
        self.apikeyRepo = apikeyRepo

    def authorize(self, user, password):
        user = self.userRepo.findUser(user, password)
        if not user:
            raise NotFound('Incorrect user and/or password')
        apikey = self.generateApikey()
        self.apikeyRepo.addTemporaryApikey(apikey, self._APIKEY_LIFETIME)
        return apikey
    
    def generateApikey(self):
        return secrets.token_hex(self._APIKEY_LENGTH)
        
