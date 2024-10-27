from fasthtml.common import *
from .navbar import navbar
from .hero import hero
from .ctas import ctas
from .footer import footer


def landing_page():
    return Section(
        navbar(),
        hero(),
        ctas(),
        footer(),
        cls="pt-16",
    )
