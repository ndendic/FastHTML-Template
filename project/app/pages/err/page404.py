from fasthtml.common import *
from fasthtml.svg import *
from ..templates.template import page_template
from fh_frankenui.core import *


@page_template("404 - App Name")
def custom_404_handler(request):
    return Section(
        Div(
            Div(
                H1(
                    "404",
                ),
                P(
                    "Something's missing.",
                ),
                P(
                    "Sorry, we can't find that page. You'll find lots to explore on the home page.",
                ),
                A(
                    "Back to Homepage",
                    href="/",
                ),
                cls="mx-auto max-w-screen-sm text-center",
            ),
            cls="py-8 px-4 mx-auto max-w-screen-xl lg:py-16 lg:px-6",
        ),
    )
