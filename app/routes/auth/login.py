import logging
from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.auth.login import login_page
from app.services.auth.auth_service import AuthService
from app.components.toaster import add_custom_toast
from fasthtml.core import APIRouter

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
            include={"email": True, "id": True}
        )
        return RedirectResponse(url="/dashboard", status_code=303)
    else:
        add_custom_toast(
            request.session, f"Failed login attempt for user: {email}", "error"
        )
        return login_page()
