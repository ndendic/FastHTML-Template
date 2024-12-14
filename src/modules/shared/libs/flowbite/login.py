from fasthtml.common import *
from shad4fast import *
from lucide_fasthtml import Lucide
from .navbar import Navbar


def social_button(icon_name, text, cls=""):
    return Button(
        Lucide(icon_name, cls="mr-2 size-4"),
        text,
        variant="outline",
        cls=f"w-full {cls}",
    )


def login_page():
    return Body(
        Card(
            CardHeader(
                CardTitle("Welcome back", cls="text-2xl"),
            ),
            CardContent(
                # Social login buttons
                Div(
                    social_button("chrome", "Log in with Google"),
                    social_button("apple", "Log in with Apple", "mt-2"),
                    cls="space-y-2",
                ),
                # Divider
                # Div(
                #     Separator(
                #         Span(
                #             "or",
                #             cls="bg-background px-2 text-muted-foreground"
                #         ),
                #         cls="my-8"
                #     ),
                #     cls="relative flex justify-center"
                # ),
                # Login form
                Form(
                    # Email field
                    Div(
                        Label("Email", htmlFor="email"),
                        Input(
                            id="email",
                            type="email",
                            placeholder="name@example.com",
                            required=True,
                        ),
                        cls="space-y-2",
                    ),
                    # Password field
                    Div(
                        Label("Password", htmlFor="password"),
                        Input(id="password", type="password", required=True),
                        cls="space-y-2",
                    ),
                    # Remember me and forgot password
                    Div(
                        Div(
                            Checkbox(id="remember"),
                            Label(
                                "Remember me",
                                htmlFor="remember",
                                cls="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                            ),
                            cls="flex items-center space-x-2",
                        ),
                        Button(
                            "Forgot password?",
                            variant="link",
                            cls="px-0 font-normal",
                        ),
                        cls="flex items-center justify-between",
                    ),
                    # Submit button
                    Button("Sign in to your account", cls="w-full mt-6"),
                    cls="space-y-4",
                ),
                # Sign up link
                Div(
                    P(
                        "Don't have an account?",
                        Button("Sign up here", variant="link", cls="px-2 font-normal"),
                        cls="text-sm text-muted-foreground text-center",
                    ),
                    cls="mt-4",
                ),
            ),
            cls="w-full max-w-md",
            standard=True,
        ),
        cls="min-h-screen flex items-center justify-center p-4",
    )
