import secrets

from app.components.toaster import setup_custom_toasts
from fasthtml.common import *
from fh_frankenui.core import *
from route_collector import add_routes

frankenui_headers = Theme.rose.headers()


login_redir = RedirectResponse("/auth/login", status_code=303)


def user_auth_before(req, sess):
    auth = req.scope["user"] = sess.get("user", None)
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
        r"/about",
        r"/pricing",
        r"/api/.*",
        "/",
    ],
)


app, rt = fast_app(
    before=beforeware,
    middleware=middleware,
    static_path="/static",
    live=True,
    pico=False,
    hdrs=frankenui_headers,
)

setup_custom_toasts(app)
app = add_routes(app)

if __name__ == "__main__":
    serve(reload=True, port=8000)
