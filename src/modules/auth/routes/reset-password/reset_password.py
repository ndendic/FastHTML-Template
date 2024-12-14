import logging

from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.components.reset_password.reset_pass import reset_pass_page
from modules.auth.services.auth_service import AuthService
from modules.shared.validators import validate_password
from modules.shared.toaster import add_custom_toast

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
