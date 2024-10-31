import logging
from supabase import AClient, create_async_client
from gotrue.types import User as GotrueUser
from decouple import config
from ..models.auth.models import User
import json

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SupabaseAuth:
    client: AClient | None = None
    is_admin: bool = False

    async def set_client(self, is_admin=False) -> AClient:
        if is_admin:
            self.client = await create_async_client(
                config("SUPABASE_URL"), config("SUPABASE_SERVICE_KEY")
            )
            self.is_admin = True
        else:
            self.client = await create_async_client(
                config("SUPABASE_URL"), config("SUPABASE_KEY")
            )
            self.is_admin = False
        return self.client

    async def get_client(self, is_admin=False) -> AClient:
        if self.client and self.is_admin == is_admin:
            return self.client
        return await self.set_client(is_admin)

    async def login(self, request, email, password):
        try:
            client = await self.get_client()
            response = await client.auth.sign_in_with_password(
                {"email": email, "password": password}
            )
            if response.user:
                request.session["auth_session"] = response.session.model_dump_json(
                    include={"access_token": True, "refresh_token": True}
                )
                return self._get_user(response.user)

            return None
        except Exception as e:
            logger.error(f"Supabase login error: {e}")
            return None

    async def login_otp(self, request, email, password):
        try:
            client = await self.get_client()
            response = await client.auth.verify_otp(
                {"email": email, "token": password, "type": "email"}
            )
            if response.user:
                request.session["auth_session"] = response.session.model_dump_json(
                    include={"access_token": True, "refresh_token": True}
                )
                return self._get_user(response.user)
            return None
        except Exception as e:
            logger.error(f"Supabase login error: {e}")
            return None

    async def oauth_login(self, request, provider, code: str = None):
        try:
            if code:
                client = await self.get_client()
                response = await client.auth.exchange_code_for_session(
                    params={"provider": "google", "auth_code": code}
                )
                if response.user:
                    request.session["auth_session"] = response.session.model_dump_json(
                        include={"access_token": True, "refresh_token": True}
                    )
                    return self._get_user(response.user)
                return None
            else:
                client = await self.get_client()
                response = await client.auth.sign_in_with_oauth(
                    {
                        "provider": provider,
                        "options": {
                            "redirect_to": f"http://localhost:5001/auth/oauth/{provider}"
                        },
                    }
                )
                if response.url:
                    return response.url
        except Exception as e:
            logger.error(f"Supabase logout error: {e}")
            return False

    async def logout(self, request, session):
        try:
            client = await self.get_client()
            response = await client.auth.sign_out()
            session.clear()
            return True
        except Exception as e:
            logger.error(f"Supabase logout error: {e}")
            return False

    async def register(self, request, password, email):
        try:
            client = await self.get_client()
            response = await client.auth.sign_up({"email": email, "password": password})
            if response.user:
                return self._get_user(response.user)
            return None
        except Exception as e:
            logger.error(f"Supabase registration error: {e}")
            return None

    async def request_password_reset(self, request, email):
        try:
            client = await self.get_client()
            await client.auth.reset_password_email(
                email,
                options={"redirect_to": "http://localhost:5001/auth/otp/"},
            )
            return True
        except Exception as e:
            logger.error(f"Supabase password reset request error: {e}")
            return False

    async def reset_password(self, request, token, new_password):
        try:
            client = await self.get_client()
            auth_session = json.loads(request.session.get("auth_session"))
            access_token = auth_session.get("access_token")
            refresh_token = auth_session.get("refresh_token")
            await client.auth.set_session(access_token, refresh_token)
            await client.auth.update_user({"password": new_password})
            return True
        except Exception as e:
            logger.error(f"Supabase password reset error: {e}")
            return False

    def _get_user(self, aut_user: GotrueUser) -> User:
        user: User = User.get(aut_user.id)
        if user:
            return user
        else:
            new_user = User.upsert(data=aut_user.user.model_dump())
            return new_user
