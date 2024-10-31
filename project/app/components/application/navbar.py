from fasthtml.common import *

# from components import Navbar
from fh_frankenui.core import *

hotkeys = [
    ("Profile", "⇧⌘P"),
    ("Billing", "⌘B"),
    ("Settings", "⌘S"),
    ("New Team", ""),
    ("Logout", "", "/auth/logout"),
]


def NavSpacedLi(t, s, href="#"):
    return Li(A(DivFullySpaced(P(t), P(s, cls=TextFont.muted_sm)), href=href))


avatar_dropdown = Div(
    DiceBearAvatar("Alicia Koch", 8, 8),
    DropDownNavContainer(
        NavHeaderLi("sveltecult", NavSubtitle("leader@sveltecult.com")),
        *[NavSpacedLi(*hk) for hk in hotkeys],
    ),
)
top_nav = NavBarContainer(
    NavBarLSide(
        NavBarNav(
            Li(A("Overview")),
            Li(A("Customers")),
            Li(A("Products")),
            Li(A("Settings")),
            cls="flex items-center",
        )
    ),
    NavBarRSide(
        NavBarNav(Input(placeholder="Search"), avatar_dropdown, cls="flex items-center")
    ),
)
