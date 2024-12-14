from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.services.auth_service import AuthService

rt = APIRouter()
auth_service = AuthService()


@rt("/auth/logout")
async def get(request):
    # Handle GET request
    result = await auth_service.logout(request, request.session)
    if result:
        return RedirectResponse(url="/", status_code=303)
    else:
        return RedirectResponse(url=request.base_url, status_code=303)


@rt("/auth/logout")
def post(request):
    # Handle POST request
    return {"message": "Received a POST request"}


# Add other HTTP methods as needed
