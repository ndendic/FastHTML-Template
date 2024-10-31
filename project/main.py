import secrets

from app.components.toaster import setup_custom_toasts
from app.pages.err.page404 import custom_404_handler
from fasthtml.common import *
from route_collector import add_routes
from fh_frankenui.core import *

frankenui_headers = Theme.rose.headers()


login_redir = RedirectResponse("/auth/login", status_code=303)


def user_auth_before(req, sess):
    auth = req.scope["auth"] = sess.get("auth", None)
    if not auth:
        return login_redir


middleware = [Middleware(SessionMiddleware, secret_key=secrets.token_urlsafe(32))]
beforeware = Beforeware(
    user_auth_before,
    skip=[
        r"/favicon\.ico",
        r"/static/.*",
        r".*\.css",
        r".*\.js",
        r"/auth/.*",
        r"/api/.*",
        "/",
    ],
)


app, rt = fast_app(
    before=beforeware,
    middleware=middleware,
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
