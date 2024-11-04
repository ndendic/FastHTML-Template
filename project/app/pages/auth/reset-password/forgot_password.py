from fasthtml.common import *
from starlette.responses import RedirectResponse
from app.components.auth.reset_password.forgot_pass import forgot_pass_page
from app.services.auth.auth_service import AuthService
from app.utils.validators import validate_email
from app.components.toaster import add_custom_toast
from fasthtml.core import APIRouter

auth_service = AuthService()

rt = APIRouter()


@rt("/auth/forgot-password")
def get(request):
    return forgot_pass_page()


@rt("/auth/forgot-password")
async def post(request):
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
