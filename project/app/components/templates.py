from typing import Any
from fasthtml.common import Div, H1, Main, P
from ..utils.decorators import template
from .landing.navbar import navbar

def PageLayout(*args: Any, **kwargs: Any):
    """Dashboard layout for all our dashboard views"""
    return Main(
        navbar(),
        Div(*args, **kwargs),
        cls="bg-white dark:bg-gray-900 min-h-screen w-full flex flex-col justify-center  pt-16",
    )


@template(Main, cls="dashboard")
def dashboard_content(*args: Any, **kwargs: Any):
    """Example component using the component_wrapper decorator"""
    return Div(
        H1("Dashboard Content"),
        P("This content is wrapped in the dashboard layout"),
        *args,
        **kwargs,
    )
