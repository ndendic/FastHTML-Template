import json

from fasthtml.common import *
from monsterui.core import *
from starlette.responses import RedirectResponse

from modules.admin.components.navbar import TopNav
from modules.admin.components.sidebar import Sidebar
from modules.public.components.navbar import Navbar


def is_htmx(request=None):
    "Check if the request is an HTMX request"
    return request and "hx-request" in request.headers


def site_page(title, content):
    return Title(title), Body(
        Navbar(),
        Main(cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12")(
            Div(cls="grid grid-cols-1 md:grid-cols-3 gap-8")(
                content, cls="min-h-screen bg-background font-sans antialiased"
            ),
        ),
    )


def page_template(title="FastWeb-App"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            content = func(request)
            if is_htmx(request):
                return content
            return site_page(title, content)
        return wrapper
    return decorator


def app_page(title, request, content):
    return Title(title), Body(
        TopNav(request),
        Div(cls="flex")(
            Sidebar(request),
            Main(
                cls="w-3/4 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4",
            )(
                Div(cls="grid grid-cols-1 md:grid-cols-3 gap-8", id="content")(
                    content,
                    cls="min-h-screen bg-background font-sans antialiased",
                )
            ),
        ),
    )


def app_template(title="App", requieres=None):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if requieres:
                user_privileges = request.session.get("priviledges", [])
                is_admin = json.loads(request.user).get("is_admin")
                if not is_admin:
                    if requieres not in user_privileges:
                        return RedirectResponse("/unauthorized", status_code=303)
            content = func(request)
            if is_htmx(request):
                return content
            return app_page(title, request, content)

        return wrapper

    return decorator


