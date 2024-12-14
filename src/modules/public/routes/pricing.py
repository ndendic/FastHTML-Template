from fasthtml.common import *
from fasthtml.core import APIRouter
from fh_frankenui import *
from fh_frankenui.core import *

from modules.shared.templates import page_template

rt = APIRouter()


def PricingHeader():
    return Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
        Div(cls="mx-auto max-w-2xl text-center")(
            H1(
                "Simple, transparent pricing",
                cls="text-4xl font-bold tracking-tight sm:text-6xl",
            ),
            P(
                "Choose the perfect plan for your needs. All plans include our core features.",
                cls=TextFont.muted_lg + " mt-6",
            ),
        )
    )


def PricingTiers():
    tiers = [
        {
            "id": "524123",
            "name": "Starter",
            "price": "$49",
            "description": "Perfect for small projects and individual developers",
            "features": [
                "All core features",
                "Up to 5 team members",
                "5GB storage",
                "Basic support",
                "Community access",
            ],
            "highlight": False,
            "cta": "Buy Now",
        },
        {
            "id": "pro",
            "name": "Pro",
            "price": "$99",
            "description": "Best for growing teams and businesses",
            "features": [
                "Everything in Starter",
                "Up to 20 team members",
                "20GB storage",
                "Priority support",
                "API access",
                "Advanced analytics",
            ],
            "highlight": True,
            "cta": "Get Started",
        },
        {
            "id": "enterprise",
            "name": "Enterprise",
            "price": "Custom",
            "description": "For large organizations with custom needs",
            "features": [
                "Everything in Pro",
                "Unlimited team members",
                "Unlimited storage",
                "24/7 dedicated support",
                "Custom integrations",
                "SLA guarantee",
            ],
            "highlight": False,
            "cta": "Contact Sales",
        },
    ]

    return Div(
        cls="isolate mx-auto mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3 max-w-7xl"
    )(
        *[
            Card(
                Div(cls="p-8" + (" bg-primary" if tier["highlight"] else ""))(
                    H2(
                        tier["name"],
                        cls="text-lg font-semibold leading-8"
                        + (" text-white" if tier["highlight"] else ""),
                    ),
                    P(
                        cls="mt-4 text-sm leading-6"
                        + (
                            " text-white/70"
                            if tier["highlight"]
                            else " text-muted-foreground"
                        )
                    )(tier["description"]),
                    P(cls="mt-6 flex items-baseline gap-x-1")(
                        Span(
                            tier["price"],
                            cls="text-4xl font-bold"
                            + (" text-white" if tier["highlight"] else ""),
                        ),
                        Span(
                            "/month",
                            cls="text-sm font-semibold"
                            + (
                                " text-white/70"
                                if tier["highlight"]
                                else " text-muted-foreground"
                            ),
                        ),
                    ),
                    A(
                        Button(
                            tier["cta"],
                            cls=(
                                "w-full mt-6 "
                                + (
                                    ButtonT.secondary
                                    if tier["highlight"]
                                    else ButtonT.primary
                                )
                            ),
                        ),
                        href=f"/subs/create-checkout/{tier['id']}",
                    ),
                    Ul(cls="mt-8 space-y-3 text-sm leading-6", role="list")(
                        *[
                            Li(
                                cls="flex gap-x-3"
                                + (" text-white" if tier["highlight"] else "")
                            )(
                                UkIcon(
                                    "check",
                                    cls="size-5 text-primary"
                                    + (" text-white" if tier["highlight"] else ""),
                                ),
                                feature,
                            )
                            for feature in tier["features"]
                        ]
                    ),
                )
            )
            for tier in tiers
        ]
    )


def ComparisonSection():
    features = [
        (
            "Core Features",
            ["Authentication", "Database Setup", "API Endpoints", "Admin Panel"],
        ),
        (
            "Team Features",
            ["Team Management", "Role-based Access", "Audit Logs", "Team Analytics"],
        ),
        (
            "Support",
            ["Documentation", "Community Forum", "Email Support", "Priority Support"],
        ),
        ("Security", ["2FA", "SSO", "Data Encryption", "Security Audits"]),
    ]

    return Div(cls="py-24 sm:py-32")(
        Div(cls="mx-auto max-w-7xl px-6 lg:px-8")(
            Div(cls="mx-auto max-w-2xl lg:text-center")(
                H2(
                    "Feature Comparison",
                    cls="text-3xl font-bold tracking-tight sm:text-4xl",
                ),
                P(
                    "Detailed breakdown of what's included in each plan",
                    cls=TextFont.muted_lg + " mt-6",
                ),
            ),
            Table(
                cls="mt-16 w-full border-collapse text-left block overflow-x-auto sm:table"
            )(
                Thead(cls="bg-muted")(
                    Tr(
                        Th("Features", cls="py-4 px-6 font-semibold"),
                        Th("Starter", cls="py-4 px-6 font-semibold"),
                        Th("Pro", cls="py-4 px-6 font-semibold"),
                        Th("Enterprise", cls="py-4 px-6 font-semibold"),
                    )
                ),
                Tbody(
                    *[
                        Tr(
                            Td(category, cls="py-4 px-6 font-medium border-t"),
                            *[
                                Td(
                                    UkIcon(
                                        "check" if i < len(items) else "x",
                                        cls=f"size-5 {'text-primary' if i < len(items) else 'text-muted-foreground'}",
                                    ),
                                    cls="py-4 px-6 border-t text-center",
                                )
                                for i in range(3)
                            ],
                        )
                        for category, items in features
                    ]
                ),
            ),
        )
    )


@rt("/pricing")
@page_template(title="Pricing - SaaS Boilerplate")
def get(request):
    return Div(cls="py-24 sm:py-32")(
        PricingHeader(),
        PricingTiers(),
        ComparisonSection(),
    )
