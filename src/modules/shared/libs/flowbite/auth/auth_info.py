from fasthtml.common import *
from fasthtml.svg import *


def auth_info_section():
    return Html(
        Div(
            Div(
                A(
                    Img(
                        src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg",
                        alt="logo",
                        cls="w-8 h-8 mr-2",
                    ),
                    "supa_saas",
                    href="/",
                    cls="inline-flex items-center mb-6 text-2xl font-semibold text-gray-900 lg:mb-10 dark:text-white",
                ),
                Div(
                    Svg(
                        Path(
                            fill_rule="evenodd",
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z",
                            clip_rule="evenodd",
                        ),
                        fill="currentColor",
                        viewbox="0 0 20 20",
                        xmlns="http://www.w3.org/2000/svg",
                        cls="w-5 h-5 mr-2 text-primary-600 shrink-0",
                    ),
                    Div(
                        H3(
                            "Get started quickly",
                            cls="mb-2 text-xl font-bold leading-none text-gray-900 dark:text-white",
                        ),
                        P(
                            "Integrate with developer-friendly APIs or choose low-code.",
                            cls="mb-2 font-light text-gray-500 dark:text-gray-400",
                        ),
                    ),
                    cls="flex",
                ),
                Div(
                    Svg(
                        Path(
                            fill_rule="evenodd",
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z",
                            clip_rule="evenodd",
                        ),
                        fill="currentColor",
                        viewbox="0 0 20 20",
                        xmlns="http://www.w3.org/2000/svg",
                        cls="w-5 h-5 mr-2 text-primary-600 shrink-0",
                    ),
                    Div(
                        H3(
                            "Support any business model",
                            cls="mb-2 text-xl font-bold leading-none text-gray-900 dark:text-white",
                        ),
                        P(
                            "Host code that you don't want to share with the world in private.",
                            cls="mb-2 font-light text-gray-500 dark:text-gray-400",
                        ),
                    ),
                    cls="flex pt-8",
                ),
                Div(
                    Svg(
                        Path(
                            fill_rule="evenodd",
                            d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z",
                            clip_rule="evenodd",
                        ),
                        fill="currentColor",
                        viewbox="0 0 20 20",
                        xmlns="http://www.w3.org/2000/svg",
                        cls="w-5 h-5 mr-2 text-primary-600 shrink-0",
                    ),
                    Div(
                        H3(
                            "Join millions of businesses",
                            cls="mb-2 text-xl font-bold leading-none text-gray-900 dark:text-white",
                        ),
                        P(
                            "supa_saas is trusted by ambitious startups and enterprises of every size.",
                            cls="mb-2 font-light text-gray-500 dark:text-gray-400",
                        ),
                    ),
                    cls="flex pt-8",
                ),
            ),
            Nav(
                Ul(
                    Li(
                        A(
                            "About",
                            href="#",
                            cls="text-sm text-gray-500 hover:underline hover:text-gray-900 dark:text-gray-400 dark:hover:text-white",
                        )
                    ),
                    Li(
                        A(
                            "Term & Conditions",
                            href="#",
                            cls="text-sm text-gray-500 hover:underline hover:text-gray-900 dark:text-gray-400 dark:hover:text-white",
                        )
                    ),
                    Li(
                        A(
                            "Contact",
                            href="#",
                            cls="text-sm text-gray-500 hover:underline hover:text-gray-900 dark:text-gray-400 dark:hover:text-white",
                        )
                    ),
                    cls="flex space-x-4",
                )
            ),
            cls="flex-col justify-between hidden mr-auto lg:flex lg:col-span-5 xl:col-span-6 xl:mb-0",
        ),
        Div(
            A(
                Img(
                    src="https://flowbite.s3.amazonaws.com/blocks/marketing-ui/logo.svg",
                    alt="logo",
                    cls="w-8 h-8 mr-2",
                ),
                "supa_saas",
                href="/",
                cls="inline-flex items-center text-2xl font-semibold text-gray-900 lg:hidden dark:text-white",
            ),
            cls="mb-6 text-center lg:hidden",
        ),
    )
