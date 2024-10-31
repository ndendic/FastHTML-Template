from fasthtml.common import *
from fasthtml.core import APIRouter
from app.services.auth_service import AuthService

rt = APIRouter()
auth_service = AuthService()


@rt("/register")
async def get(request):
    return Titled(
        "Register",
        H1("Register"),
        Form(
            Label("Email:", For="email"),
            Input(type="email", name="email", id="email", required=True),
            Label("Password:", For="password"),
            Input(type="password", name="password", id="password", required=True),
            Button("Register", type="submit"),
            action="/register",
            method="POST",
        ),
    )


@rt("/register")
async def post(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JSONResponse(
                {"error": "Email and password are required"}, status=400
            )

        user = await auth_service.register(request, password, email)
        if user:
            return JSONResponse({"message": "Registration successful"})
        return JSONResponse({"error": "Registration failed"}, status=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status=500)
