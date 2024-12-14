from fasthtml.common import *

from modules.public.components.ctas import ctas
from modules.public.components.footer import footer
from modules.public.components.hero import hero
from modules.public.components.navbar import Navbar


def landing_page():
    return Section(
        Navbar(),
        hero(),
        ctas(),
        footer(),
        cls="pt-16",
    )
