from fasthtml.common import *
from fasthtml.svg import *


def navbar():
    return Nav(
        Div(
            A(
                Img(
                    src="https://flowbite.com/docs/images/logo.svg",
                    alt="Flowbite Logo",
                    cls="h-8",
                ),
                Span(
                    "supa_saas",
                    cls="self-center text-2xl font-semibold whitespace-nowrap dark:text-white",
                ),
                href="https://flowbite.com/",
                cls="flex items-center space-x-3 rtl:space-x-reverse",
            ),
            Div(
                A(
                    Button(
                        "Login",
                        type="button",
                        cls="text-white bg-primary-700 hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
                    ),
                    href="/auth/login",
                ),
                Button(
                    Span("Open main menu", cls="sr-only"),
                    Svg(
                        Path(
                            stroke="currentColor",
                            stroke_linecap="round",
                            stroke_linejoin="round",
                            stroke_width="2",
                            d="M1 1h15M1 7h15M1 13h15",
                        ),
                        aria_hidden="true",
                        xmlns="http://www.w3.org/2000/svg",
                        fill="none",
                        viewbox="0 0 17 14",
                        cls="w-5 h-5",
                    ),
                    data_collapse_toggle="navbar-sticky",
                    type="button",
                    aria_controls="navbar-sticky",
                    aria_expanded="false",
                    cls="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600",
                ),
                cls="flex md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse",
            ),
            Div(
                Ul(
                    Li(
                        A(
                            "Home",
                            href="#",
                            aria_current="page",
                            cls="block py-2 px-3 text-white bg-primary-700 rounded md:bg-transparent md:text-primary-700 md:p-0 md:dark:text-primary-500",
                        )
                    ),
                    Li(
                        A(
                            "About",
                            href="#",
                            cls="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-primary-700 md:p-0 md:dark:hover:text-primary-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700",
                        )
                    ),
                    Li(
                        A(
                            "Services",
                            href="#",
                            cls="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-primary-700 md:p-0 md:dark:hover:text-primary-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700",
                        )
                    ),
                    Li(
                        A(
                            "Contact",
                            href="#",
                            cls="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-primary-700 md:p-0 md:dark:hover:text-primary-500 dark:text-white dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700",
                        )
                    ),
                    cls="flex flex-col p-4 md:p-0 mt-4 font-medium border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700",
                ),
                id="navbar-sticky",
                cls="items-center justify-between hidden w-full md:flex md:w-auto md:order-1",
            ),
            cls="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4",
        ),
        cls="bg-white dark:bg-gray-900 fixed w-full z-20 top-0 start-0 border-b border-gray-200 dark:border-gray-600",
    )
