from fasthtml.common import *
from app.models import User
from app.models import BaseTable
from typing import List

# from components import Navbar
from fh_frankenui.core import *


tables = [
    (
        model.sidebar_icon,
        model.display_name,
        f"/table/{model.__name__.lower()}",
    )
    for model in BaseTable.__subclasses__()
    if model.sidebar_item
]


discoved_data = [
    ("play-circle", "Listen Now"),
    ("binoculars", "Browse"),
    ("rss", "Radio"),
]
library_data = [
    ("play-circle", "Playlists"),
    ("music", "Songs"),
    ("user", "Made for You"),
    ("users", "Artists"),
    ("bookmark", "Albums"),
]
playlists_data = [("library", "Recently Added"), ("library", "Recently Played")]


def SidebarButton(icon, text, href="#"):
    return Li(
        A(
            DivLAligned(
                UkIcon(icon),
                P(text),
                cls="space-x-2",
            ),
            href=href + "#",
            hx_boost="true",
            hx_target="#content",
            hx_swap_oob=True,
        )
    )


def SidebarGroup(text, data):
    return NavParentLi(
        A(H4(text)),
        NavContainer(parent=False)(*[SidebarButton(*o) for o in data]),
    )


def Sidebar(request):
    return Div(cls="h-screen sticky top-0 border-r border-border px-4")(
        NavContainer(uk_nav=True, parent=True)(
            SidebarGroup("Tables", tables),
            SidebarGroup("Discover", discoved_data),
            SidebarGroup("Library", library_data),
            SidebarGroup("Playlists", playlists_data),
            cls=(NavT.primary, "space-y-3", "w-60"),
        )
    )
