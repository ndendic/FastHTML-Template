from fasthtml.common import *
from fasthtml.svg import *
from fh_frankenui.core import *


def forgot_pass_page():
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))("supa_app"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.large)(
                '"Secure account recovery made simple - get back to what matters most."'
            ),
            Footer(cls=TextT.small)("Security Team"),
        ),
    )

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(
            A(
                Button("Back to Login", cls=ButtonT.ghost, submit=False),
                href="/auth/login",
            )
        ),
        DivCentered(cls="flex-1")(
            Div(cls=f"space-y-6 w-[350px]")(
                Div(cls="flex flex-col space-y-2 text-center")(
                    H3("Password Recovery"),
                    P(cls=TextFont.muted_sm)(
                        "Enter your email address and we'll send you a One Time Password"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    Input(
                        placeholder="name@example.com",
                        name="email",
                        id="email",
                        type="email",
                    ),
                    Button(
                        UkIcon("mail", cls="mr-2"),
                        "Send One Time Password",
                        cls=(ButtonT.primary, "w-full"),
                    ),
                    DividerLine(),
                    P(cls=(TextFont.muted_sm, "text-center"))(
                        "Remember your password? ",
                        A(
                            cls="underline underline-offset-4 hover:text-primary",
                            href="/auth/login",
                        )("Sign in"),
                    ),
                ),
            )
        ),
    )

    return Grid(left, right, cols=2, gap=0, cls="h-screen")
