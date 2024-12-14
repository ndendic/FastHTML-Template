import logging

from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.components.reset_password.forgot_pass import forgot_pass_page
from modules.auth.services.auth_service import AuthService
from modules.shared.validators import validate_email
from modules.shared.toaster import add_custom_toast

logger = logging.getLogger(__name__)
auth_service = AuthService()

rt = APIRouter()


@rt("/auth/forgot-password")
def get(request):
    return forgot_pass_page()


@rt("/auth/forgot-password")
async def post(request):
    logger.debug("Handling forgot password request")
    form = await request.form()
    email = form.get("email")
    if not email or not validate_email(email):
        add_custom_toast(
            request.session, "Please provide a valid email address", "error"
        )
        return forgot_pass_page()
    if await auth_service.request_password_reset(request, email):
        add_custom_toast(
            request.session, "Password reset link sent to email", "success"
        )
        return RedirectResponse(url=f"/auth/otp?email={email}", status_code=303)
    else:
        add_custom_toast(
            request.session, "Unable to process password reset request", "error"
        )
        return forgot_pass_page()
