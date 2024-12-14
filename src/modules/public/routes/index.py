# app/pages/index.py
from fasthtml.common import *
from fasthtml.core import APIRouter
from fh_frankenui import *
from fh_frankenui.core import *

from modules.shared.templates import page_template

rt = APIRouter()


def HeroSection():
    return Div(cls="py-24 px-6 lg:px-8 bg-background")(
        Div(cls="mx-auto max-w-3xl text-center")(
            H1(
                "Build faster with our SaaS Boilerplate",
                cls="text-4xl font-bold tracking-tight sm:text-6xl",
            ),
            P(
                "Launch your SaaS project in minutes, not months. Everything you need to start building your next great idea.",
                cls=TextFont.muted_lg + " mt-6",
            ),
            Div(cls="mt-10 flex items-center justify-center gap-x-6")(
                Button("Get Started", cls=ButtonT.primary + " text-lg px-8 py-3"),
                A(
                    "Learn more",
                    href="#features",
                    cls="text-lg font-semibold leading-6",
                ),
            ),
        )
    )


def FeatureSection():
    features = [
        (
            "rocket",
            "Quick Setup",
            "Get up and running in less than 5 minutes with our streamlined setup process.",
        ),
        (
            "shield",
            "Built-in Security",
            "Enterprise-grade security features included out of the box.",
        ),
        (
            "database",
            "Database Ready",
            "Pre-configured database setup with migrations and models.",
        ),
        (
            "layout",
            "Modern UI",
            "Beautiful, responsive UI components powered by FrankenUI.",
        ),
        (
            "code",
            "Developer Friendly",
            "Well-documented codebase with best practices baked in.",
        ),
        (
            "users",
            "Auth & Users",
            "Complete authentication and user management system.",
        ),
    ]

    return Div(cls="py-24 bg-muted/50", id="features")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2(
                    "Everything you need to build faster",
                    cls="text-base font-semibold leading-7 text-primary",
                ),
                P(
                    "Complete Feature Set",
                    cls="mt-2 text-3xl font-bold tracking-tight sm:text-4xl",
                ),
                P(
                    "Our boilerplate includes everything you need to build a modern SaaS application.",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Div(cls="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none")(
                Grid(
                    *[
                        Card(
                            UkIcon(icon, cls="size-7 text-primary"),
                            H3(title, cls="mt-6 text-xl font-semibold"),
                            P(desc, cls=TextFont.muted_sm + " mt-4"),
                            cls="relative p-8 hover:bg-muted/50 transition-colors m-5",
                        )
                        for icon, title, desc in features
                    ],
                    cols_lg=3,
                    cols_md=2,
                    cols_sm=1,
                    gap=8,
                    cls="lg:max-w-none",
                )
            ),
        )
    )


def CTASection():
    return Div(cls="bg-primary py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl text-center")(
                H2(
                    "Ready to get started?",
                    cls="text-3xl font-bold tracking-tight text-white sm:text-4xl",
                ),
                P(
                    "Start building your next great idea today with our complete SaaS boilerplate.",
                    cls="mx-auto mt-6 max-w-xl text-lg leading-8 text-white/80",
                ),
                Div(cls="mt-10 flex items-center justify-center gap-x-6")(
                    Button("Get started", cls=ButtonT.secondary + " text-lg px-8 py-3"),
                    A(
                        "Contact sales",
                        href="/contact",
                        cls="text-white hover:text-white/90 text-lg font-semibold leading-6",
                    ),
                ),
            )
        )
    )


@rt("/")
@page_template(title="SaaS Boilerplate - Build Faster")
def get(request):
    return Div(HeroSection(), FeatureSection(), CTASection())
