from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.services.auth_service import AuthService

auth_service = AuthService()

rt = APIRouter()


@rt("/auth/oauth/{provider}")
async def get(request, provider: str = ""):
    code = request.query_params.get("code") or None

    if code:
        user = await auth_service.oauth_login(request, provider, code)
        if user:
            request.session["user"] = user.model_dump_json(
                include={"email": True, "id": True, "is_admin": True}
            )
            request.session["priviledges"] = user.priviledges

            return RedirectResponse(url="/dashboard", status_code=303)
    else:
        url = await auth_service.oauth_login(request, provider)
        if url:
            return RedirectResponse(url=url, status_code=303)
        else:
            return {"message": "Failed to get OAuth login URL"}


@rt("/auth/oauth/{provider}")
def post(request):
    # Handle POST request
    return {"message": "Received a POST request"}


# Add other HTTP methods as needed
