import logging
import secrets
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import asyncio
import bcrypt

from app.models.auth.models import User
from fasthtml.oauth import GoogleAppClient, redir_url
from decouple import config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FastHTMLAuth:
    def __init__(self):
        self.reset_tokens = {}

    async def login(self, request, email, password):
        try:
            user = User.get_by_email(email)
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
            return None
        except Exception as e:
            logger.error(f"FastHTML login error: {e}")
            return None

    async def oauth_login(self, request, provider, code: str = None):
        # TODO: Implement this method with fasthtml
        auth_callback_path = f"oauth/{provider}"
        redir = redir_url(auth_callback_path)
        client = GoogleAppClient(
            client_id=config("GOOGLE_OAUTH_ID"),
            client_secret=config("GOOGLE_OAUTH_KEY"),
        )
        return client.base_url

    async def logout(self, request, session):
        session.clear()
        return True

    async def register(self, request, password, email):
        try:
            if User.get_by_email(email):
                return None
            hashed_password = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            user = User()
            user.password = hashed_password
            user.email = email
            user.save()
            return user
        except Exception as e:
            logger.error(f"FastHTML registration error: {e}")
            return None

    async def request_password_reset(self, request, email):
        try:
            user = User.get_by_email(email)
            if user:
                token = secrets.token_urlsafe()
                self.reset_tokens[token] = {
                    "email": user.email,
                    "expires": time.time() + 3600,
                }  # 1 hour expiry
                await self._send_reset_email(email, token)
                return True
            return False
        except Exception as e:
            logger.error(f"FastHTML password reset request error: {e}")
            return False

    async def reset_password(self, request, token, new_password):
        try:
            token_data = self.reset_tokens.get(token)
            if token_data and time.time() < token_data["expires"]:
                email = token_data["email"]
                hashed_password = bcrypt.hashpw(
                    new_password.encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                # self.users.update({"password": hashed_password}, email)TODO
                del self.reset_tokens[token]
                return True
            return False
        except Exception as e:
            logger.error(f"FastHTML password reset error: {e}")
            return False

    async def _send_reset_email(self, email, token):
        # TODO: Implement this method with Resend
        smtp_server = config("SMTP_SERVER")
        smtp_port = config("SMTP_PORT")
        smtp_username = config("SMTP_USERNAME")
        smtp_password = config("SMTP_PASSWORD")
        reset_url = f"{config('BASE_URL')}/reset-password/{token}"

        msg = MIMEMultipart()
        msg["From"] = smtp_username
        msg["To"] = email
        msg["Subject"] = "Password Reset Request"

        body = f"Click the following link to reset your password: {reset_url}"
        msg.attach(MIMEText(body, "plain"))

        try:
            await asyncio.get_event_loop().run_in_executor(
                None,
                self._send_email,
                smtp_server,
                smtp_port,
                smtp_username,
                smtp_password,
                msg,
            )
            logger.info(f"Password reset email sent to {email}")
        except Exception as e:
            logger.error(f"Error sending password reset email: {e}")

    def _send_email(self, smtp_server, smtp_port, smtp_username, smtp_password, msg):
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
