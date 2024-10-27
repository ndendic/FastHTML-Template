from fasthtml.common import *
from fasthtml.svg import *
from ..auth_info import auth_info_section
from ...landing.navbar import navbar


def otp(email: str = None):
    return Section(
        navbar(),
        Div(
            auth_info_section(),
            Div(
                H1(
                    "Sign in with One Time Password",
                    cls="mb-1 text-xl font-bold leading-tight tracking-tight text-gray-900 sm:text-2xl dark:text-white",
                ),
                P(
                    "Your One Time Password (OTP) has been sent to your email address.",
                    cls="font-light text-gray-500 dark:text-gray-400",
                ),
                Form(
                    Div(
                        Label(
                            "Email",
                            fr="email",
                            cls="block mb-2 text-sm font-medium text-gray-900 dark:text-white",
                        ),
                        Input(
                            type="email",
                            name="email",
                            value=email,
                            id="email",
                            placeholder="Enter your email",
                            required="",
                            cls="bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                        ),
                    ),
                    Div(
                        Label(
                            "One Time Password (OTP)",
                            fr="password",
                            cls="block mb-2 text-sm font-medium text-gray-900 dark:text-white",
                        ),
                        Input(
                            type="password",
                            name="otp_password",
                            id="otp_password",
                            placeholder="••••••••",
                            required="",
                            cls="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-600 focus:border-primary-600 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500",
                        ),
                    ),
                    Div(
                        Div(
                            Input(
                                id="terms",
                                aria_describedby="terms",
                                type="checkbox",
                                required="",
                                cls="w-4 h-4 border border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:bg-gray-700 dark:border-gray-600 dark:focus:ring-primary-600 dark:ring-offset-gray-800",
                            ),
                            cls="flex items-center h-5",
                        ),
                        Div(
                            Label(
                                "I agree to supa_saas’s",
                                A(
                                    "Terms of Use",
                                    href="#",
                                    cls="font-medium text-primary-600 dark:text-primary-500 hover:underline",
                                ),
                                "and",
                                A(
                                    "Privacy Policy",
                                    href="#",
                                    cls="font-medium text-primary-600 dark:text-primary-500 hover:underline",
                                ),
                                ".",
                                fr="terms",
                                cls="text-gray-500 dark:text-gray-300",
                            ),
                            cls="ml-3 text-sm",
                        ),
                        cls="flex items-start",
                    ),
                    Div(
                        Button(
                            "Sign in",
                            type="submit",
                            cls="text-white bg-primary-600 hover:bg-primary-700 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
                        ),
                        A(
                            "Return to login",
                            href="/auth/login",
                            cls="text-sm text-primary-600 dark:text-primary-500 hover:underline",
                        ),
                        cls="flex items-center space-x-3",
                    ),
                    method="post",
                    cls="mt-4 space-y-4 lg:mt-5 lg:space-y-5",
                ),
                cls="w-full col-span-6 p-6 mx-auto bg-white rounded-lg shadow dark:bg-gray-800 md:mt-0 sm:max-w-lg sm:p-8",
            ),
            cls="max-w-screen-xl px-4 py-8 mx-auto lg:grid lg:gap-20 lg:py-16 lg:grid-cols-12",
        ),
        Script("""
            (function() {
                const fragment = window.location.hash.substring(1); // Get fragment after #
                const params = new URLSearchParams(fragment); // Parse it as query params
                const authToken = params.get('access_token'); // Extract 'auth_token'

                if (authToken) {
                    // Get the current URL
                    const currentUrl = new URL(window.location.href);

                    // Add the authToken as a query parameter
                    currentUrl.searchParams.set('access_token', authToken);

                    // Redirect to the new URL with the authToken query parameter
                    window.location.href = currentUrl.toString();
                }
            })();
        """),
        cls="pt-16 bg-gray-50 dark:bg-gray-900",
    )
