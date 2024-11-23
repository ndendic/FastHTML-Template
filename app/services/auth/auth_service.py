import logging
from .fasthtml_auth import FastHTMLAuth
from app.components.toaster import add_custom_toast

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self):
        self.auth = FastHTMLAuth()

    async def login(self, request, email, password):
        """Handle user login."""
        try:
            return await self.auth.login(request, email, password)
        except Exception as e:
            logger.error(f"Login error: {e}")
            return None

    async def oauth_login(self, request, provider, code=None):
        """Handle OAuth login."""
        try:
            return await self.auth.oauth_login(request, provider, code)
        except Exception as e:
            logger.error(f"OAuth login error: {e}")
            return None

    async def logout(self, request, session):
        """Handle user logout."""
        try:
            return await self.auth.logout(request, session)
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False

    async def register(self, request, password, email):
        """Handle user registration."""
        try:
            return await self.auth.register(request, password, email)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return None

    async def request_password_reset(self, request, email):
        """Handle password reset request."""
        try:
            return await self.auth.request_password_reset(request, email)
        except Exception as e:
            logger.error(f"Password reset request error: {e}")
            return False

    async def reset_password(self, request, token, new_password):
        """Handle password reset."""
        try:
            return await self.auth.reset_password(request, token, new_password)
        except Exception as e:
            logger.error(f"Password reset error: {e}")
            return False

    async def login_otp(self, request, email, password):
        """Handle OTP login."""
        try:
            return await self.auth.login_otp(request, email, password)
        except Exception as e:
            logger.error(f"OTP login error: {e}")
            return None
