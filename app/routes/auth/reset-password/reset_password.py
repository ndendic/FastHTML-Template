import logging

from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.auth.reset_password.reset_pass import reset_pass_page
from app.services.auth.auth_service import AuthService
from app.utils.validators import validate_password
from app.components.toaster import add_custom_toast
from fasthtml.core import APIRouter

logger = logging.getLogger(__name__)
auth_service = AuthService()

rt = APIRouter()


@rt("/auth/reset-password")
def get(request: str = None):
    return reset_pass_page()


@rt("/auth/reset-password")
async def post(request, access_token):
    logger.debug("Handling reset password request")
    form = await request.form()
    new_password = form.get("new_password")
    if not new_password or not validate_password(new_password):
        add_custom_toast(
            request.session, "Password must be at least 8 characters long", "error"
        )
        return reset_pass_page()
    if await auth_service.reset_password(request, access_token, new_password):
        add_custom_toast(request.session, "Password reset successful", "success")
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        add_custom_toast(request.session, "Password reset failed", "error")
        return reset_pass_page()
