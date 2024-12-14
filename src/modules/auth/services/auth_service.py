import logging

from decouple import config

from modules.auth.services.fasthtml_auth import FastHTMLAuth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.auth = FastHTMLAuth()

    async def login(self, request, email, password):
        return await self.auth.login(request, email, password)

    async def oauth_login(self, request, provider, code=None):
        return await self.auth.oauth_login(request, provider, code)

    async def logout(self, request, session):
        return await self.auth.logout(request, session)

    async def register(self, request, password, email):
        return await self.auth.register(request, password, email)

    async def request_password_reset(self, request, email):
        return await self.auth.request_password_reset(request, email)

    async def reset_password(self, request, token, new_password):
        return await self.auth.reset_password(request, token, new_password)

    async def login_otp(self, request, email, password):
        return await self.auth.login_otp(request, email, password)
