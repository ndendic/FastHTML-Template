from fasthtml.common import *
from fasthtml.core import APIRouter
from app.services.auth_service import AuthService

rt = APIRouter()
auth_service = AuthService()


@rt("/login")
async def get(request):
    return Titled(
        "Login",
        H1("Login"),
        Form(
            Label("Email:", For="email"),
            Input(type="email", name="email", id="email", required=True),
            Label("Password:", For="password"),
            Input(type="password", name="password", id="password", required=True),
            Button("Login", type="submit"),
            action="/login",
            method="POST",
        ),
    )


@rt("/login")
async def post(request):
    try:
        data = await request.json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JSONResponse(
                {"error": "Email and password are required"}, status=400
            )

        user = await auth_service.login(request, email, password)
        if user:
            return JSONResponse({"message": "Login successful"})
        return JSONResponse({"error": "Invalid credentials"}, status=401)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status=500)
