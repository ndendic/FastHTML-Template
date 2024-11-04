from fasthtml.common import *
from fasthtml.svg import *
from fh_frankenui.core import *


def registration_page():
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))("supa_app"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.large)(
                '"This library has saved me countless hours of work and helped me deliver stunning designs to my clients faster than ever before."'
            ),
            Footer(cls=TextT.small)("Sofia Davis"),
        ),
    )

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(
            A(Button("Login", cls=ButtonT.ghost, submit=False), href="/auth/login")
        ),
        DivCentered(cls="flex-1")(
            Div(cls=f"space-y-6 w-[350px]")(
                Div(cls="flex flex-col space-y-2 text-center")(
                    H3("Create an account"),
                    P(cls=TextFont.muted_sm)(
                        "Pick your favorite way to authenticate with us"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    A(
                        Button(
                            UkIcon("github", cls="mr-2"),
                            "Github",
                            cls=(ButtonT.default, "w-full"),
                            submit=False,
                        ),
                        href="/auth/oauth/google",
                    ),
                    DividerSplit("Or continue with", cls=TextFont.muted_sm),
                    Input(
                        placeholder="name@example.com",
                        name="email",
                        id="email",
                        type="email",
                    ),
                    Input(
                        placeholder="••••••••",
                        name="password",
                        id="password",
                        type="password",
                    ),
                    Button(
                        # Span(cls="mr-2", uk_spinner="ratio: 0.54"),
                        UkIcon("mail", cls="mr-2"),
                        "Sign up with Email",
                        cls=(ButtonT.primary, "w-full"),
                        # disabled=True,
                    ),
                ),
                P(cls=(TextFont.muted_sm, "text-center"))(
                    "By clicking continue, you agree to our ",
                    A(
                        cls="underline underline-offset-4 hover:text-primary",
                        href="#demo",
                        uk_toggle=True,
                    )("Terms of Service"),
                    " and ",
                    A(
                        cls="underline underline-offset-4 hover:text-primary",
                        href="#demo",
                        uk_toggle=True,
                    )("Privacy Policy"),
                    ".",
                ),
            )
        ),
    )

    return Grid(left, right, cols=2, gap=0, cls="h-screen")
