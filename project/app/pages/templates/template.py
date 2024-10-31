from fasthtml.common import *
from fh_frankenui.core import *
from fh_frankenui import *
from ...components.application.navbar import top_nav
from ...components.landing.navbar import Navbar


def page_template(title="FastSaas"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            content = func(request)
            return Title(title), Body(
                Navbar(),
                Main(
                    cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12"
                )(  # Added py-12 for vertical padding
                    Div(cls="grid grid-cols-1 md:grid-cols-3 gap-8")(
                        content, cls="min-h-screen bg-background font-sans antialiased"
                    )
                ),
            )

        return wrapper

    return decorator


def app_template(title="FastSaas"):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            content = func(request)
            return Title(title), Body(
                Div(cls="border-b border-border px-4")(top_nav),
                Main(cls="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4")(
                    Div(cls="grid grid-cols-1 md:grid-cols-3 gap-8")(
                        content, cls="min-h-screen bg-background font-sans antialiased"
                    )
                ),
            )

        return wrapper

    return decorator
