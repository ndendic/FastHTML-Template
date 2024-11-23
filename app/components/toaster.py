from fastcore.xml import FT
from fasthtml.core import *
from fasthtml.components import *
from fasthtml.xtend import *
from fasthtml.svg import *

tcid = "fh-toast-container"
sk = "toasts"
toast_css = """
.fh-toast-container {
    position: fixed; top: 20px; left: 85%; transform: translateX(-50%); z-index: 1000;
    display: flex; flex-direction: column; align-items: center; width: 100%;
    pointer-events: none; opacity: 0; transition: opacity 0.3s ease-in-out;
}
.fh-toast {
    background-color: #333; color: white;
    padding: 12px 20px; border-radius: 4px; margin-bottom: 10px;
    max-width: 80%; width: auto; text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.fh-toast-info { background-color: #2196F3; }
.fh-toast-success { background-color: #4CAF50; }
.fh-toast-warning { background-color: #FF9800; }
.fh-toast-error { background-color: #F44336; }
"""

toast_js = """
export function proc_htmx(sel, func) {
  htmx.onLoad(elt => {
    const elements = any(sel, elt, false);
    if (elt.matches && elt.matches(sel)) elements.unshift(elt);
    elements.forEach(func);
  });
}
proc_htmx('.fh-toast-container', async function(toast) {
    await sleep(100);
    toast.style.opacity = '0.8';
    await sleep(3000);
    toast.style.opacity = '0';
    await sleep(300);
    toast.remove();
});
"""


def add_custom_toast(sess, message, typ="info"):
    assert typ in (
        "info",
        "success",
        "warning",
        "error",
    ), '`typ` not in ("info", "success", "warning", "error")'
    sess.setdefault(sk, []).append((message, typ))


def toast(typ: str, msg: str) -> Div:
    return Div(
        toast_icon(typ),
        Div(msg, cls="ms-3 text-sm font-normal"),
        Button(
            Span("Close", cls="sr-only"),
            Svg(
                Path(
                    stroke="currentColor",
                    stroke_linecap="round",
                    stroke_linejoin="round",
                    stroke_width="2",
                    d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6",
                ),
                aria_hidden="true",
                xmlns="http://www.w3.org/2000/svg",
                fill="none",
                viewbox="0 0 14 14",
                cls="w-3 h-3",
            ),
            type="button",
            data_dismiss_target=f"#toast-{typ}",
            aria_label="Close",
            cls="ms-auto -mx-1.5 -my-1.5 rounded-lg focus:ring-2 p-1.5 inline-flex items-center justify-center h-8 w-8",
        ),
        id=f"toast-{typ}",
        role="alert",
        cls="flex items-center bg-background w-full max-w-xs p-4 mb-4 rounded-lg shadow",
    )


def render_toasts(sess):
    toasts = [toast(typ, msg) for msg, typ in sess.pop(sk, [])]
    return Div(Div(*toasts, cls="fh-toast-container"), hx_swap_oob="afterbegin:body")


def toast_after(resp, req, sess):
    if sk in sess and (not resp or isinstance(resp, (tuple, FT))):
        req.injects.append(render_toasts(sess))


def setup_custom_toasts(app):
    app.hdrs += (Style(toast_css), Script(toast_js, type="module"))
    app.after.append(toast_after)


def toast_icon(typ: str) -> Div:
    if (typ == "info") or (typ == "success"):
        return (
            Div(
                Svg(
                    Path(
                        d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"
                    ),
                    aria_hidden="true",
                    xmlns="http://www.w3.org/2000/svg",
                    fill="currentColor",
                    viewbox="0 0 20 20",
                    cls="w-5 h-5",
                ),
                Span("Check icon", cls="sr-only"),
                cls="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-green-500 bg-green-100 rounded-lg dark:bg-green-800 dark:text-green-200",
            ),
        )
    elif typ == "error":
        return Div(
            Svg(
                Path(
                    d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z"
                ),
                aria_hidden="true",
                xmlns="http://www.w3.org/2000/svg",
                fill="currentColor",
                viewbox="0 0 20 20",
                cls="w-5 h-5",
            ),
            Span("Error icon", cls="sr-only"),
            cls="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-red-500 bg-red-100 rounded-lg dark:bg-red-800 dark:text-red-200",
        )
    else:
        return Div(
            Svg(
                Path(
                    d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"
                ),
                aria_hidden="true",
                xmlns="http://www.w3.org/2000/svg",
                fill="currentColor",
                viewbox="0 0 20 20",
                cls="w-5 h-5",
            ),
            Span("Warning icon", cls="sr-only"),
            cls="inline-flex items-center justify-center flex-shrink-0 w-8 h-8 text-orange-500 bg-orange-100 rounded-lg dark:bg-orange-700 dark:text-orange-200",
        )
