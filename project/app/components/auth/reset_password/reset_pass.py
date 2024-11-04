from fasthtml.common import *
from fasthtml.svg import *
from fh_frankenui.core import *


def reset_pass_page():
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))("supa_app"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.large)(
                '"A strong password is random, long, and unique. Never reuse passwords across multiple accounts."'
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
                    H3("Create New Password"),
                    P(cls=TextFont.muted_sm)(
                        "Your new password must be different from previously used passwords"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    Input(
                        placeholder="••••••••",
                        name="new_password",
                        id="new_password",
                        type="password",
                    ),
                    Input(
                        placeholder="Confirm password",
                        name="confirm_password",
                        id="confirm_password",
                        type="password",
                    ),
                    Button(
                        UkIcon("key", cls="mr-2"),
                        "Reset Password",
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
