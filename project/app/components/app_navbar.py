from fasthtml.common import *
from fasthtml.svg import *


def app_navbar():
    return Header(
        Nav(
            Div(
                Div(
                    A(
                        Img(
                            src="https://flowbite.s3.amazonaws.com/logo.svg",
                            alt="Flowbite Logo",
                            cls="mr-3 h-8",
                        ),
                        Span(
                            "supa_saas",
                            cls="self-center text-2xl font-semibold whitespace-nowrap dark:text-white",
                        ),
                        href="https://flowbite.com",
                        cls="flex mr-6",
                    ),
                    cls="flex justify-start items-center",
                ),
                Div(
                    A(
                        "My profile",
                        href="#",
                        cls="font-medium text-primary-600 dark:text-primary-500 hover:underline",
                    ),
                    Div(cls="h-4 w-px mx-2 border dark:border-gray-700"),
                    A(
                        "Logout",
                        href="/auth/logout",
                        cls="font-medium text-primary-600 dark:text-primary-500 hover:underline",
                    ),
                    cls="flex justify-between items-center text-sm space-x-4 lg:order-2",
                ),
                cls="flex justify-between items-center",
            ),
            cls="bg-white border-gray-200 px-4 py-3 dark:bg-gray-900",
        ),
        Nav(
            Div(
                Div(
                    Ul(
                        Li(
                            A(
                                "Overview",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="block lg:inline",
                        ),
                        Li(
                            A(
                                "Sales",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="block lg:inline",
                        ),
                        Li(
                            A(
                                "Billing",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="block lg:inline",
                        ),
                        Li(
                            A(
                                "Team",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="md:block lg:inline hidden",
                        ),
                        Li(
                            A(
                                "Resources",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="md:block lg:inline hidden",
                        ),
                        Li(
                            A(
                                "Messages",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="md:block lg:inline hidden",
                        ),
                        Li(
                            A(
                                "Support",
                                href="#",
                                cls="inline-block px-3 py-2 rounded-lg hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            cls="md:block lg:inline hidden",
                        ),
                        Li(
                            Button(
                                Svg(
                                    Path(
                                        d="M6 10a2 2 0 11-4 0 2 2 0 014 0zM12 10a2 2 0 11-4 0 2 2 0 014 0zM16 12a2 2 0 100-4 2 2 0 000 4z"
                                    ),
                                    xmlns="http://www.w3.org/2000/svg",
                                    viewbox="0 0 20 20",
                                    fill="currentColor",
                                    cls="h-5 w-5",
                                ),
                                id="navigationDropdownButton",
                                aria_expanded="false",
                                data_dropdown_toggle="navigationDropdown",
                                cls="inline-flex items-center justify-center px-2 py-2 rounded-xl hover:text-gray-900 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-white",
                            ),
                            Div(
                                Ul(
                                    Li(
                                        A(
                                            "Overview",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Sales",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Billing",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Team",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Resources",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Messages",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    Li(
                                        A(
                                            "Support",
                                            href="#",
                                            cls="flex items-center py-2 px-4 text-sm hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white",
                                        )
                                    ),
                                    aria_labelledby="navigationDropdownButton",
                                    cls="py-1 text-gray-700 dark:text-gray-300",
                                ),
                                id="navigationDropdown",
                                cls="hidden z-50 my-4 w-56 text-base list-none bg-white rounded-xl divide-y divide-gray-100 shadow dark:bg-gray-700 dark:divide-gray-600",
                            ),
                            cls="block md:hidden",
                        ),
                        cls="flex items-center text-sm text-gray-600 font-medium",
                    ),
                    cls="flex items-center",
                ),
                cls="px-4 py-2",
            ),
            id="toggleMobileMenu",
            cls="bg-gray-50 border-b border-gray-200 dark:bg-gray-700 dark:border-gray-900",
        ),
    )
