import json
import logging

from fasthtml.common import *
from fasthtml.core import APIRouter

from modules.auth.components.profile_forms import profile_page
from modules.auth.models import User
from modules.auth.services.auth_service import AuthService
from modules.shared.templates import app_template
from modules.shared.toaster import add_custom_toast

logger = logging.getLogger(__name__)
auth_service = AuthService()

rt = APIRouter()
UPLOAD_DIR = Path("assets/uploads/avatars")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@rt("/user/profile")
@app_template("Profile")
def get(request):
    return profile_page(request)


@rt("/upload-avatar", methods=["POST"])
async def upload_avatar(request):
    try:
        async with request.form() as form:
            if "avatar" not in form:
                return P("No file selected", cls="text-red-500 mt-4")

            file = form["avatar"]
            if not hasattr(file, "filename"):
                return P("Invalid file upload", cls="text-red-500 mt-4")

            user_data = json.loads(request.session.get("user"))
            user = User.get(user_data["id"])

            # Read file content
            content = await file.read()

            # Save file to local storage
            file_path = UPLOAD_DIR / f"avatar_{user.id}_{file.filename}"
            file_path.write_bytes(content)

            # Update user's avatar_url
            avatar_url = f"assets/uploads/avatars/{file_path.name}"
            user.avatar_url = avatar_url
            user.save()

            # Return success message and refresh the main avatar
            return Div(
                P("Avatar updated successfully!", cls="text-green-500"),
                Script("""
                    // Refresh the main avatar image
                    setTimeout(() => {
                        window.location.reload();
                    }, 1000);
                """),
                cls="mt-4",
            )

    except Exception as e:
        return P(f"Error: {str(e)}", cls="text-red-500 mt-4")


@rt("/update-profile", methods=["POST"])
async def update_profile(request):
    try:
        async with request.form() as form:
            user_data = json.loads(request.session.get("user"))
            user = User.get(user_data["id"])

            # Update user fields
            user.full_name = form.get("full_name", user.full_name)
            user.email = form.get("email", user.email)
            # user.user_metadata = json.loads(form.get("user_metadata", "{}"))

            user.save()
            add_custom_toast(
                request.session, "Profile updated successfully!", "success"
            )

            # return None
            return P("Profile updated successfully!", cls="text-green-500 mt-4")

    except Exception as e:
        return P(f"Error: {str(e)}", cls="text-red-500 mt-4")