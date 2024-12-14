from fasthtml.common import *
from fasthtml.core import APIRouter

from modules.auth.components.reset_password.otp import otp_page
from modules.auth.services.auth_service import AuthService
from modules.shared.toaster import add_custom_toast

rt = APIRouter()

auth_service = AuthService()


@rt("/auth/otp")
def get(request, email: str = None):
    if request.query_params.get("email"):
        email = request.query_params.get("email")
    return otp_page(email)


@rt("/auth/otp")
async def post(request, access_token: str = None):
    form = await request.form()
    email = form.get("email")
    password = form.get("otp_password")
    if not email or not password:
        add_custom_toast(request.session, "Username and password are required", "error")
        return otp_page()
    user = await auth_service.login_otp(request, email, password)
    if user:
        request.session["user"] = user.model_dump_json(
            include={"email": True, "id": True, "is_admin": True}
        )
        request.session["priviledges"] = user.priviledges
        return RedirectResponse(url="/auth/reset-password", status_code=303)
    else:
        add_custom_toast(request.session, f"Failed login attempt for user: {email}")
        return otp_page()


# Add other HTTP methods as needed
