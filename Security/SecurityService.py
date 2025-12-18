from flask import abort, g
from datetime import datetime, timedelta, timezone
from werkzeug.exceptions import TooManyRequests, Forbidden, Unauthorized

class SecurityService:
    apikeyRepo = None
    requestRepo = None

    def __init__(self, apikeyRepo, requestRepo):
        self.apikeyRepo = apikeyRepo
        self.requestRepo = requestRepo

    def authorize(self, request):
        apikey = request.headers.get('X-API-KEY')

        if not apikey:
            raise Unauthorized('API KEY required')
            abort(401, "API key required")

        apikeyInfo = self.validateApikey(apikey)
        self.checkRateLimit(apikeyInfo)
        self.registerRequest(apikey, request)
        g.apikey = apikeyInfo


    def validateApikey(self, apikey):
        key = self.apikeyRepo.findOne(apikey)

        if not key:
            raise Forbidden("Invalid API KEY")

        return key
    
    
    def checkRateLimit(self, apikeyInfo):
        timestampFrom = datetime.now(timezone.utc) - timedelta(seconds=3600)
        count = self.requestRepo.countRequestsByApikeyAndIp(apikeyInfo['apikey'], timestampFrom)

        if count >= apikeyInfo["limit"]:
            raise TooManyRequests("Rate limit excedido")
        
        
    def registerRequest(self, apikey, request):
        self.requestRepo.register(apikey, request.path, request.remote_addr)