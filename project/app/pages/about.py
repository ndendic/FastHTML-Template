from fasthtml.common import *
from fasthtml.core import APIRouter
from fh_frankenui.core import *
from fh_frankenui import *
from ..templates import page_template

rt = APIRouter()


def CompanySection():
    return Div(cls="py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2(
                    "About Our Company",
                    cls="text-4xl font-bold tracking-tight sm:text-6xl",
                ),
                P(
                    "We're on a mission to help developers build better SaaS applications faster.",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Div(
                cls="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none text-center"
            )(
                P(
                    "Founded in 2024, we've been helping developers and companies streamline their development process. "
                    + "Our boilerplate is built on years of experience in building scalable SaaS applications.",
                    cls=TextFont.muted_lg + " mb-6",
                ),
                P(
                    "We believe in providing developers with the tools they need to focus on what matters most - "
                    + "building great products for their customers.",
                    cls=TextFont.muted_lg,
                ),
            ),
        )
    )


def TeamSection():
    team = [
        (
            "John Doe",
            "CEO & Founder",
            DiceBearAvatar("Kimberly"),
            "Previously led engineering at major tech companies",
        ),
        (
            "Jane Smith",
            "CTO",
            DiceBearAvatar("Kimberly"),
            "15+ years of experience in scalable architectures",
        ),
        (
            "Mike Johnson",
            "Head of Product",
            DiceBearAvatar("Kimberly"),
            "Product veteran with multiple successful launches",
        ),
        (
            "Sarah Williams",
            "Lead Developer",
            DiceBearAvatar("Kimberly"),
            "Open source contributor and community leader",
        ),
    ]

    return Div(cls="bg-muted/50 py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2("Our Team", cls="text-3xl font-bold tracking-tight sm:text-4xl"),
                P(
                    "Meet the people behind the product",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Div(cls="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none")(
                Grid(
                    *[
                        Card(
                            Img(
                                src=f"/static/images/{img}",
                                cls="w-24 h-24 rounded-full mx-auto",
                            ),
                            H3(name, cls="mt-6 text-xl font-semibold text-center"),
                            P(role, cls="text-primary text-center"),
                            P(desc, cls=TextFont.muted_sm + " mt-4 text-center"),
                            cls="p-8",
                        )
                        for name, role, img, desc in team
                    ],
                    cols=[1, 2, 4],
                    gap=8,
                )
            ),
        )
    )


def ValuesSection():
    values = [
        (
            "lightbulb",
            "Innovation",
            "We constantly push the boundaries of what's possible",
        ),
        (
            "heart",
            "Customer First",
            "Everything we do is focused on delivering value to our users",
        ),
        (
            "shield-check",
            "Quality",
            "We maintain the highest standards in our code and products",
        ),
        (
            "users",
            "Community",
            "We believe in the power of community and open collaboration",
        ),
    ]

    return Div(cls="py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2("Our Values", cls="text-3xl font-bold tracking-tight sm:text-4xl"),
                P(
                    "The principles that guide everything we do",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Div(cls="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none")(
                Grid(
                    *[
                        Card(
                            UkIcon(icon, cls="size-8 text-primary mx-auto"),
                            H3(title, cls="mt-6 text-xl font-semibold text-center"),
                            P(desc, cls=TextFont.muted_sm + " mt-4 text-center"),
                            cls="p-8",
                        )
                        for icon, title, desc in values
                    ],
                    cols=[1, 2, 4],
                    gap=8,
                )
            ),
        )
    )


@rt("/about")
@page_template(title="About Us - SaaS Boilerplate")
def get(request):
    return Div(CompanySection(), TeamSection(), ValuesSection())


def post(request):
    # Handle POST request
    return {"message": "Received a POST request"}


# Add other HTTP methods as needed
