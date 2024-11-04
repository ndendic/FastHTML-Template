from fasthtml.common import *
from fasthtml.svg import *
from fh_frankenui.core import *


def otp_page(email: str = None):
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))("supa_app"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.large)(
                '"Two-factor authentication adds an extra layer of security to your account by requiring more than just a password to sign in."'
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
                    H3("Sign in with OTP"),
                    P(cls=TextFont.muted_sm)(
                        "Please enter the one-time password sent to your email"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    Input(
                        value=email,
                        placeholder="name@example.com",
                        name="email",
                        id="email",
                        type="email",
                        disabled=True if email else False,
                    ),
                    Input(
                        placeholder="Enter OTP Code",
                        name="otp_password",
                        id="otp_password",
                        type="text",
                    ),
                    Button(
                        UkIcon("lock", cls="mr-2"),
                        "Verify OTP",
                        hx_post="/auth/otp",
                        hx_vals={"email": email, "password": "otp_password"},
                        hx_swap="none",
                        cls=(ButtonT.primary, "w-full"),
                    ),
                    DividerLine(),
                    P(cls=(TextFont.muted_sm, "text-center"))(
                        "Didn't receive the code? ",
                        A(
                            "Resend OTP",
                            href="#",
                            hx_post="/auth/forgot-password",
                            hx_vals={"email": email},
                            hx_swap="none",
                            cls="underline underline-offset-4 hover:text-primary",
                        ),
                    ),
                ),
            )
        ),
    )

    return Grid(left, right, cols=2, gap=0, cls="h-screen")
