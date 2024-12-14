from fasthtml.common import *
from .navbar import Navbar
from .hero import hero
from .ctas import ctas
from .footer import footer


def landing_page():
    return Section(
        hero(),
        ctas(),
        footer(),
    )
