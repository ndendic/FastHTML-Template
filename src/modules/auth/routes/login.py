import logging

from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.components.login import login_page
from modules.auth.services.auth_service import AuthService
from modules.shared.toaster import add_custom_toast

logger = logging.getLogger(__name__)
auth_service = AuthService()

rt = APIRouter()


@rt("/auth/login")
def get(request):
    return login_page()


@rt("/auth/login")
async def post(request):
    logger.debug("Handling login request")
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    if not email or not password:
        add_custom_toast(request.session, "Username and password are required", "error")
        return login_page()
    user = await auth_service.login(request, email, password)
    if user:
        request.session["user"] = user.model_dump_json(
            include={"email": True, "id": True, "is_admin": True}
        )
        request.session["priviledges"] = user.priviledges
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        add_custom_toast(
            request.session, f"Failed login attempt for user: {email}", "error"
        )
        return login_page()
