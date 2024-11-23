import json
from fasthtml.common import *
from app.models import User

# from components import Navbar
from fh_frankenui.core import *

hotkeys = [
    ("Profile", "⇧⌘P", "/user/profile"),
    ("Billing", "⌘B"),
    ("Settings", "⌘S"),
    ("New Team", ""),
    ("Logout", "", "/auth/logout", False),
]


def NavSpacedLi(t, s, href="#", is_content=True):
    return Li(
        A(
            DivFullySpaced(P(t), P(s, cls=TextFont.muted_sm)),
            href=href + "#",
            hx_boost="true" if is_content else "false",
            hx_target="#content",
            hx_swap_oob=True,
        )
    )


def Avatar(
    url,
    h=20,  # Height
    w=20,  # Width
):  # Span with Avatar
    return Span(
        cls=f"relative flex h-{h} w-{w} shrink-0 overflow-hidden rounded-full bg-accent"
    )(
        Img(
            cls=f"aspect-square h-{h} w-{w}",
            alt="Avatar",
            loading="lazy",
            src=url,
        )
    )


def avatar_dropdown(request):
    user_data = request.session.get("user")
    if user_data:
        user_data = json.loads(user_data)
        user = User.get(user_data["id"])
        if user:
            return Div(
                Avatar(user.avatar_url, 8, 8)
                if user.avatar_url
                else DiceBearAvatar("Destiny", 8, 8),
                DropDownNavContainer(
                    NavHeaderLi(user.full_name, NavSubtitle(user.email)),
                    *[NavSpacedLi(*hk) for hk in hotkeys],
                ),
            )
    return None


def TopNav(request):
    return NavBarContainer(
        NavBarLSide(
            NavBarNav(
                Li(A("Dashboard", href="/dashboard")),
                Li(A("Tables")),
                Li(A("Products")),
                Li(A("Settings")),
                cls="flex items-center",
            )
        ),
        NavBarRSide(
            NavBarNav(
                Input(placeholder="Search"),
                avatar_dropdown(request),
                cls="flex items-center",
            )
        ),
    )


def Navbar(request):
    return top_nav(request)
