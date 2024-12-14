import json

from fasthtml.common import *

from monsterui.core import *

from modules.auth.models import User

hotkeys = [
    ("Profile", "⇧⌘P", "/user/profile"),
    ("Billing", "⌘B"),
    ("Settings", "⌘S"),
    ("New Team", ""),
    ("Logout", "", "/auth/logout", False),
]


def NavSpacedLi(t, s=None, href="#", is_content=True):
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


def theme_toggle():
    return Button(
        UkIcon(icon="moon"),
        Script("""
            function initializeTheme() {
                const themeToggle = document.getElementById('theme-toggle');
                if (!themeToggle) return;
                
                const icon = themeToggle.querySelector('uk-icon');
                const htmlElement = document.documentElement;
                
                // Check initial theme
                if (
                    localStorage.getItem("mode") === "dark" ||
                    (!("mode" in localStorage) &&
                    window.matchMedia("(prefers-color-scheme: dark)").matches)
                ) {
                    htmlElement.classList.add("dark");
                    icon.setAttribute('icon', 'sun');
                } else {
                    htmlElement.classList.remove("dark");
                    icon.setAttribute('icon', 'moon');
                }
                
                // Toggle theme
                themeToggle.addEventListener('click', () => {
                    const isDark = htmlElement.classList.contains('dark');
                    
                    if (isDark) {
                        htmlElement.classList.remove('dark');
                        localStorage.setItem('mode', 'light');
                        icon.setAttribute('icon', 'moon');
                    } else {
                        htmlElement.classList.add('dark');
                        localStorage.setItem('mode', 'dark');
                        icon.setAttribute('icon', 'sun');
                    }
                });
            }

            // Initialize when DOM is loaded
            document.addEventListener('DOMContentLoaded', initializeTheme);
            // Re-initialize when HTMX content is loaded (if you're using HTMX)
            document.addEventListener('htmx:afterSettle', initializeTheme);
        """),
        id="theme-toggle",
        cls=ButtonT.ghost + " flex items-center justify-center",
    )


def TopNav(request):
    return NavBarContainer(
        NavBarLSide(
            NavBarNav(
                NavSpacedLi("Dashboard", href="/dashboard"),
                NavSpacedLi("Blog", href="/blog"),
                NavSpacedLi("Documentation", href="/docs"),
                NavSpacedLi("Contact", href="/contact"),
                cls="flex items-center ml-16",
            )
        ),
        NavBarRSide(
            DivRAligned(
                theme_toggle(),
                # Input(placeholder="Search"),
                avatar_dropdown(request),
                cls="space-x-2",
            )
        ),
        cls="sticky top-0 border-b border-border px-4 z-100 bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    )


nav_items = [
    ("Dashboard", "/dashboard"),
    ("Blog", "/blog"),
    ("Documentation", "/docs"),
    ("Contact", "/contact"),
]


def MobileDrawer():
    return Div(
        Button(
            UkIcon("menu", height=24, width=24),
            cls=ButtonT.ghost + " md:hidden",
            uk_toggle="target: #mobile-menu",
        ),
        Modal(
            Div(cls="p-6 bg-background")(
                H3("Menu", cls="text-lg font-semibold mb-4"),
                NavContainer(
                    *[
                        Li(
                            A(
                                label,
                                href=url,
                                cls="flex items-center p-2 hover:bg-muted rounded-lg transition-colors",
                            )
                        )
                        for label, url in nav_items
                    ],
                    Li(DividerLine(lwidth=2, y_space=4)),
                    Li(
                        A(
                            "Sign in",
                            href="/auth/login",
                            cls="flex items-center p-2 hover:bg-muted rounded-lg transition-colors",
                        )
                    ),
                    Li(
                        Button(
                            "Get Started",
                            cls=ButtonT.primary + " w-full mt-2",
                            onclick="window.location.href='/pricing'",
                        )
                    ),
                    cls=NavT.primary + " space-y-2",
                ),
            ),
            id="mobile-menu",
        ),
    )


def NewNav(request):
    return Header(
        cls="sticky top-0 z-100 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
    )(
        Div(cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16")(
            Div(cls="flex h-full justify-between items-center")(
                Div(cls="flex items-center gap-x-8")(
                    # Mobile menu drawer
                    MobileDrawer(),
                    # Logo
                    A(href="/", cls="flex items-center")(
                        Span("app", cls="font-bold text-xl")
                    ),
                    # Desktop navigation
                    Nav(cls="hidden md:flex items-center space-x-8")(
                        *[
                            A(
                                label,
                                href=url,
                                cls="text-sm font-medium transition-colors hover:text-foreground/80 text-foreground/60",
                            )
                            for label, url in nav_items
                        ]
                    ),
                ),
                # Desktop CTA buttons
                Div(cls="hidden md:flex items-center space-x-4")(
                    theme_toggle(),
                    Input(placeholder="Search"),
                    avatar_dropdown(request),
                ),
            )
        )
    )


def Navbar(request):
    return TopNav(request)
