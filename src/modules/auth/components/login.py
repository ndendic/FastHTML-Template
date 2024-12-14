from fasthtml.common import *
from fasthtml.svg import *
from monsterui.core import *


def login_page():
    left = Div(
        cls="col-span-1 hidden flex-col justify-between bg-zinc-900 p-8 text-white lg:flex"
    )(
        Div(cls=(TextT.bold, TextT.default))("Web-App Inc"),
        Blockquote(cls="space-y-2")(
            P(cls=TextT.large)(
                '"This library has saved me countless hours of work and helped me deliver stunning designs to my clients faster than ever before."'
            ),
            Footer(cls=TextT.small)("Sofia Davis"),
        ),
    )

    right = Div(cls="col-span-2 flex flex-col p-8 lg:col-span-1")(
        DivRAligned(
            A(
                Button("Register", cls=ButtonT.ghost, submit=False),
                href="/auth/register",
            )
        ),
        DivCentered(cls="flex-1")(
            Div(cls="space-y-6 w-[350px]")(
                Div(cls="flex flex-col space-y-2 text-center")(
                    H3("Sign in to your account"),
                    P(cls=TextFont.muted_sm)(
                        "Pick your favorite way to authenticate with us"
                    ),
                ),
                Form(cls="space-y-6", method="post")(
                    A(
                        Button(
                            UkIcon("github", cls="mr-2"),
                            "Github",
                            cls=(ButtonT.default, "w-full mb-2"),
                            submit=False,
                        ),
                        href="/auth/oauth/github",
                    ),
                    A(
                        Button(
                            Svg(
                                G(
                                    Path(
                                        d="M20.3081 10.2303C20.3081 9.55056 20.253 8.86711 20.1354 8.19836H10.7031V12.0492H16.1046C15.8804 13.2911 15.1602 14.3898 14.1057 15.0879V17.5866H17.3282C19.2205 15.8449 20.3081 13.2728 20.3081 10.2303Z",
                                        fill="#3F83F8",
                                    ),
                                    Path(
                                        d="M10.7019 20.0006C13.3989 20.0006 15.6734 19.1151 17.3306 17.5865L14.1081 15.0879C13.2115 15.6979 12.0541 16.0433 10.7056 16.0433C8.09669 16.0433 5.88468 14.2832 5.091 11.9169H1.76562V14.4927C3.46322 17.8695 6.92087 20.0006 10.7019 20.0006V20.0006Z",
                                        fill="#34A853",
                                    ),
                                    Path(
                                        d="M5.08857 11.9169C4.66969 10.6749 4.66969 9.33008 5.08857 8.08811V5.51233H1.76688C0.348541 8.33798 0.348541 11.667 1.76688 14.4927L5.08857 11.9169V11.9169Z",
                                        fill="#FBBC04",
                                    ),
                                    Path(
                                        d="M10.7019 3.95805C12.1276 3.936 13.5055 4.47247 14.538 5.45722L17.393 2.60218C15.5852 0.904587 13.1858 -0.0287217 10.7019 0.000673888C6.92087 0.000673888 3.46322 2.13185 1.76562 5.51234L5.08732 8.08813C5.87733 5.71811 8.09302 3.95805 10.7019 3.95805V3.95805Z",
                                        fill="#EA4335",
                                    ),
                                    clip_path="url(#clip0_13183_10121)",
                                ),
                                Defs(
                                    Rect(
                                        width="24",
                                        height="24",
                                        fill="white",
                                        transform="translate(0.5)",
                                    ),
                                    id="clip0_13183_10121",
                                ),
                                viewbox="0 0 24 24",
                                fill="none",
                                xmlns="http://www.w3.org/2000/svg",
                                cls="w-5 h-5 mr-2",
                            ),
                            "Google",
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
                        UkIcon("mail", cls="mr-2"),
                        "Sign in with Email",
                        cls=(ButtonT.primary, "w-full"),
                    ),
                    Div(cls=(TextFont.muted_sm, "flex items-center justify-between"))(
                        A(
                            "Forgot Password?",
                            href="/auth/forgot-password",
                            cls="text-sm",
                        ),
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
