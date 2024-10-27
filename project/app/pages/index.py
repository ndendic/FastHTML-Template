from fasthtml.common import *
from app.components.home import home as Home
from app.components.landing.page import landing_page
from fasthtml.core import APIRouter
import logging

home_router = APIRouter()

logger = logging.getLogger(__name__)

rt = APIRouter()


@rt("/")
def get(request):
    user = request.session.get("user")
    if not user:
        return landing_page()
    user = request.session["user"]
    # logger.info(f"Handling home request for user:{user}")
    return Home(user)
