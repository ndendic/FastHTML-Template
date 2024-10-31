from app.components.toaster import setup_custom_toasts
from app.pages.err.page404 import custom_404_handler
from fasthtml.common import *
from route_collector import add_routes
from fh_frankenui.core import *

frankenui_headers = Theme.rose.headers()
app, rt = fast_app(
    static_path="project/static",
    live=True,
    pico=False,
    hdrs=frankenui_headers,
    exception_handlers={404: custom_404_handler},
)

setup_custom_toasts(app)
app = add_routes(app)

if __name__ == "__main__":
    serve(reload=True)
