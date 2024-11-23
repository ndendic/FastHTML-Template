import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.auth.registration import registration_page
from app.services.auth.auth_service import AuthService
from app.utils.validators import validate_email, validate_password
from app.components.toaster import add_custom_toast
from fasthtml.core import APIRouter

logger = logging.getLogger(__name__)
auth_service = AuthService()

rt = APIRouter()


@rt("/auth/register")
def get(request):
    return registration_page()


@rt("/auth/register")
async def post(request):
    logger.debug("Handling register request")
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    if not email or not password:
        add_custom_toast(request.session, "All fields are required", "error")
        return registration_page()
    if not validate_email(email):
        add_custom_toast(request.session, "Invalid email format")
        return registration_page()
    if not validate_password(password):
        add_custom_toast(request.session, "Password must be at least 8 characters long")
        return registration_page()

    user = await auth_service.register(request, password, email)
    if user:
        request.session["user"] = user.model_dump_json()
        return RedirectResponse(url="/", status_code=303)
    else:
        logger.warning(f"Failed registration attempt for user: {email}")
        add_custom_toast(
            request.session,
            "Unable to register user. Username or email may already be in use.",
            "error",
        )
        return registration_page()
