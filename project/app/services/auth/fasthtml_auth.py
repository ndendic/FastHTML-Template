import asyncio
import logging
import random
import smtplib
import time

import bcrypt
import resend
from app.models.auth.models import User
from decouple import config
from fasthtml.oauth import GoogleAppClient, redir_url
from app.components.toaster import add_custom_toast

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FastHTMLAuth:
    # Store OTPs with email and expiry
    otps = {}

    def __init__(self):
        pass

    async def login(self, request, email, password):
        try:
            user = User.get_by_email(email)
            if not user:
                add_custom_toast(
                    request.session, f"User with email {email} not found", "error"
                )
                return None
            if bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
                return user
            else:
                add_custom_toast(request.session, "Incorect Password", "error")
            return None
        except Exception as e:
            add_custom_toast(request.session, f"Login failed: {e}", "error")
            logger.error(f"FastHTML login error: {e}")
            return None

    async def login_otp(self, request, email, otp):
        """Verify OTP and login user"""
        try:
            # Validate the OTP
            if await self.validate_otp(request, email, otp):
                # Get the user
                user = User.get_by_email(email)
                if user:
                    # Clean up the OTP after successful login
                    if email in FastHTMLAuth.otps:
                        del FastHTMLAuth.otps[email]
                    return user
            return None
        except Exception as e:
            add_custom_toast(
                request.session, f"Authentication OTP login error: {e}", "error"
            )
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
            add_custom_toast(request.session, f"Registration error: {e}", "error")
            logger.error(f"FastHTML registration error: {e}")
            return None

    def _generate_otp(self) -> str:
        """Generate a 6-digit OTP"""
        return "".join([str(random.randint(0, 9)) for _ in range(6)])

    async def request_password_reset(self, request, email):
        try:
            user = User.get_by_email(email)
            if user:
                otp = self._generate_otp()
                FastHTMLAuth.otps[email] = {
                    "otp": otp,
                    "expires": time.time() + 300,  # 5 minutes expiry
                    "attempts": 0,  # Track failed attempts
                }
                await self._send_otp_email(request, email, otp)
                return True
            return False
        except Exception as e:
            add_custom_toast(
                request.session, f"Password reset request error: {e}", "error"
            )
            logger.error(f"FastHTML password reset request error: {e}")
            return False

    async def validate_otp(self, request, email, otp):
        try:
            otp_data = FastHTMLAuth.otps.get(email)
            if not otp_data:
                return False

            # Check if OTP has expired
            if time.time() > otp_data["expires"]:
                del FastHTMLAuth.otps[email]
                return False

            # Check if too many failed attempts
            if otp_data["attempts"] >= 3:
                del FastHTMLAuth.otps[email]
                return False

            # Validate OTP
            if otp_data["otp"] == otp:
                # OTP is valid - mark it as verified but don't delete yet
                # It will be deleted after password reset
                FastHTMLAuth.otps[email]["verified"] = True
                return True
            else:
                # Increment failed attempts
                FastHTMLAuth.otps[email]["attempts"] += 1
                return False

        except Exception as e:
            add_custom_toast(request.session, f"OTP validation error: {e}", "error")
            logger.error(f"FastHTML OTP validation error: {e}")
            return False

    async def reset_password(self, request, token, new_password):
        try:
            # Get email from request
            email = request.query_params.get("email")
            if not email:
                return False

            otp_data = FastHTMLAuth.otps.get(email)
            if otp_data and otp_data.get("verified"):
                user = User.get_by_email(email)
                if user:
                    hashed_password = bcrypt.hashpw(
                        new_password.encode("utf-8"), bcrypt.gensalt()
                    ).decode("utf-8")
                    user.password = hashed_password
                    user.save()
                    # Clean up the OTP after successful password reset
                    del FastHTMLAuth.otps[email]
                    return True
            return False
        except Exception as e:
            add_custom_toast(request.session, f"Password reset error: {e}", "error")
            logger.error(f"FastHTML password reset error: {e}")
            return False

    async def _send_otp_email(self, request, email, otp):
        smtp_password = config("RESEND_API_KEY")

        resend.api_key = smtp_password

        params: resend.Emails.SendParams = {
            "from": "noreply@artyficial.space",
            "to": [email],
            "subject": "Password Reset OTP",
            "html": f"""
                <h2>Password Reset Request</h2>
                <p>Your one-time password (OTP) for password reset is: <strong>{otp}</strong></p>
                <p>This OTP will expire in 5 minutes.</p>
                <p>If you did not request this password reset, please ignore this email.</p>
            """,
            "reply_to": "ndendic@artyficial.space",
        }

        try:
            email: resend.Email = resend.Emails.send(params)
            add_custom_toast(
                request.session, f"Password reset OTP sent to {email}", "info"
            )
            logger.info(f"Password reset OTP sent to {email}")
            return True
        except asyncio.TimeoutError:
            add_custom_toast(request.session, "Email sending timed out", "error")
            logger.error("Email sending timed out")
            return False
        except Exception as e:
            add_custom_toast(
                request.session, f"Error sending password reset OTP: {e}", "error"
            )
            logger.error(f"Error sending password reset OTP: {e}")
            return False

    def _send_email_sync(
        self, smtp_server, smtp_port, smtp_username, smtp_password, msg
    ):
        with smtplib.SMTP(smtp_server, smtp_port, timeout=5) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
