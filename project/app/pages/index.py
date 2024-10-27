from fasthtml.common import *
from app.components.landing.page import landing_page
from fasthtml.core import APIRouter
import logging

home_router = APIRouter()

logger = logging.getLogger(__name__)

rt = APIRouter()


@rt("/")
def get(request):
    return landing_page()

