from fasthtml.common import *
from fh_frankenui.core import *
from app.components.public import Navbar
from app.components.application.navbar import TopNav
from app.components.application.sidebar import Sidebar


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


def page_template(title="FastSaas"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            content = func(request)
            return site_page(title, content)

        return wrapper

    return decorator


def app_page(title, request, content):
    return Title(title), Body(
        Div(cls="border-b border-border px-4")(TopNav(request)),
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


def app_template(title="FastSaas"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            content = func(request)
            if is_htmx(request):
                return content
            return app_page(title, request, content)

        return wrapper

    return decorator
