import logging
import secrets

from app.components.toaster import setup_custom_toasts
from app.pages.err.page404 import custom_404_handler
from fasthtml.common import *
from route_collector import add_routes



hdrs = (
    Script(src="https://cdn.tailwindcss.com"),
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.css",
    ),
    Script(src="/tailwind.config.js"),  # Updated to use static path
)
ftrs = [Script(src="https://cdn.jsdelivr.net/npm/flowbite@2.5.2/dist/flowbite.min.js")]


app, rt = fast_app(
    static_path="project/static",
    live=True,
    pico=False,
    hdrs=hdrs,
    ftrs=ftrs,
    exception_handlers={404: custom_404_handler},
)   

setup_custom_toasts(app)
app = add_routes(app)

if __name__ == "__main__":
    serve(reload=True)
