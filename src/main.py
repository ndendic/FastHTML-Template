import logging
import secrets

# import modules
from fasthtml.common import *
from monsterui.core import *
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

from modules.shared.toaster import setup_custom_toasts
from route_collector import add_routes

# fh_cfg["auto_id"] = True

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


middleware = [Middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))]

frankenui_headers = Theme.rose.headers()

def user_auth_before(req, sess):
    auth = req.scope["user"] = sess.get("user", None)
    if not auth:
        return RedirectResponse("/auth/login", status_code=303)


beforeware = Beforeware(
    user_auth_before,
    skip=[
        r"/favicon\.ico",
        r"/assets/.*",
        r".*\.css",
        r".*\.js",
        r"/auth/.*",
        r"/pricing",
        r"/about",
        r"/contact",
        r"/api/.*",
        "/",
    ],
)


app, rt = fast_app(
    before=beforeware,
    middleware=middleware,
    static_path="assets",
    live=True,
    pico=False,
    hdrs=(
        frankenui_headers,
        HighlightJS(langs=["python", "javascript", "html", "css"]),
    ),
    # ftrs=flowbite_ftrs,
    htmlkw=dict(cls="bg-surface-light dark:bg-surface-dark"),
    # exception_handlers={404: custom_404_handler},
)

setup_custom_toasts(app)
app = add_routes(app)

if __name__ == "__main__":
    serve(reload=True)
