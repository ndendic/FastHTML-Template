from fasthtml.common import *

def hero():
    return Section(
            Div(
                Div(
                    H1(
                        "Time to buld fassst!",
                        cls="max-w-2xl mb-4 text-4xl font-extrabold tracking-tight leading-none md:text-5xl xl:text-6xl dark:text-white",
                    ),
                    P(
                        "Here at supa_app we focus on markets where technology, innovation, and capital can unlock long-term value and drive economic growth.",
                        cls="max-w-2xl mb-6 font-light text-gray-500 lg:mb-8 md:text-lg lg:text-xl dark:text-gray-400",
                    ),
                    Form(
                        Div(
                            Div(
                                Label(
                                    "Email address",
                                    fr="member_email",
                                    cls="hidden mb-2 text-sm font-medium text-gray-900 dark:text-gray-300",
                                ),
                                Input(
                                    placeholder="Enter your email",
                                    type="email",
                                    name="member[email]",
                                    id="member_email",
                                    required="",
                                    cls="block md:w-96 w-full p-3 pl-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                                ),
                                cls="relative w-auto mr-3",
                            ),
                            Div(
                                Input(
                                    type="submit",
                                    value="Try for free",
                                    name="member_submit",
                                    id="member_submit",
                                    cls="px-5 py-3 text-sm font-medium text-center text-white rounded-lg cursor-pointer bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
                                )
                            ),
                            cls="flex items-center mb-3",
                        ),
                        Div(
                            "Instant signup. No credit card required.",
                            A(
                                "Terms of Service",
                                href="#",
                                cls="text-primary-600 hover:underline dark:text-primary-500",
                            ),
                            "and",
                            A(
                                "Privacy Policy",
                                href="#",
                                cls="text-primary-600 hover:underline dark:text-primary-500",
                            ),
                            ".",
                            cls="text-sm text-left text-gray-500 dark:text-gray-300",
                        ),
                        action="#",
                        cls="",
                    ),
                    cls="mr-auto place-self-center lg:col-span-7 xl:col-span-8",
                ),
                Div(
                    Img(
                        src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/hero/mobile-app.svg",
                        alt="phone illustration",
                    ),
                    cls="hidden lg:mt-0 lg:col-span-5 xl:col-span-4 lg:flex",
                ),
                cls="grid max-w-screen-xl px-4 py-8 mx-auto lg:gap-12 xl:gap-0 lg:py-16 lg:grid-cols-12",
            ),
            cls="bg-white dark:bg-gray-900",
        ),
        