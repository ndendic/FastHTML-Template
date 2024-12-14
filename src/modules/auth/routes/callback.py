from fasthtml.common import *
from fasthtml.core import APIRouter
from starlette.responses import RedirectResponse

from modules.auth.services.auth_service import AuthService

rt = APIRouter()
auth_service = AuthService()


@rt("/auth/callback/#{access_token}")
async def get(request, access_token: str = ""):
    code = request.query_params.get("access_token") or None

    if code:
        user = await auth_service.oauth_login(request, "", code)
        if user:
            request.session["user"] = user.model_dump_json(
                include={"email": True, "id": True, "is_admin": True}
            )
            request.session["priviledges"] = user.priviledges
            return RedirectResponse(url="/", status_code=303)
    else:
        return Container(
            H1("Welcome to the Auth Page"),
            Script("""
            (function() {
                const fragment = window.location.hash.substring(1); // Get fragment after #
                const params = new URLSearchParams(fragment); // Parse it as query params
                const authToken = params.get('auth_token'); // Extract 'auth_token'

                if (authToken) {
                    // Make a POST request to send the auth token to the server
                    fetch('/store-token', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ token: authToken })
                    });
                }
            })();
        """),
        )


@rt("/auth/callback/#{access_token}")
def post(request, auth_token: str):
    # Access the auth_token from the POST request and handle it
    print(f"Received auth token: {auth_token}")
    # You can now process or store the token in the session or database
    return "Token received"


# Add other HTTP methods as needed
