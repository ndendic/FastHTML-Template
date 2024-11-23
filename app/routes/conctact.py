from fasthtml.common import *
from fasthtml.svg import *
from fasthtml.core import APIRouter
from app.routes.templates.template import page_template

rt = APIRouter()


@rt("/contact")
@page_template()
def contact_page():
    return Section(
        Div(
            Div(
                H2(
                    "Contact Us",
                    cls="mb-4 text-4xl tracking-tight font-extrabold text-white",
                ),
                P(
                    "We use an agile approach to test assumptions and connect with the needs of your audience early and often.",
                    cls="mb-16 font-light text-gray-400 sm:text-xl",
                ),
                cls="px-4 lg:pt-24 pt-8 pb-72 lg:pb-80 mx-auto max-w-screen-sm text-center lg:px-6",
            ),
            cls="bg-[url('https://flowbite.s3.amazonaws.com/blocks/marketing-ui/contact/laptop-human.jpg')] bg-no-repeat bg-cover bg-center bg-gray-700 bg-blend-multiply",
        ),
        Div(
            Form(
                Div(
                    Label(
                        "First Name",
                        fr="first-name",
                        cls="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300",
                    ),
                    Input(
                        type="text",
                        id="first-name",
                        placeholder="Bonnie",
                        required="",
                        cls="block p-3 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light",
                    ),
                ),
                Div(
                    Label(
                        "Last Name",
                        fr="last-name",
                        cls="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300",
                    ),
                    Input(
                        type="text",
                        id="last-name",
                        placeholder="Green",
                        required="",
                        cls="block p-3 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light",
                    ),
                ),
                Div(
                    Label(
                        "Your email",
                        fr="email",
                        cls="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300",
                    ),
                    Input(
                        type="email",
                        id="email",
                        placeholder="name@flowbite.com",
                        required="",
                        cls="shadow-sm bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light",
                    ),
                ),
                Div(
                    Label(
                        "Phone Number",
                        fr="phone-number",
                        cls="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-300",
                    ),
                    Input(
                        type="number",
                        id="phone-number",
                        placeholder="+12 345 6789",
                        required="",
                        cls="block p-3 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 shadow-sm focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500 dark:shadow-sm-light",
                    ),
                ),
                Div(
                    Label(
                        "Your message",
                        fr="message",
                        cls="block mb-2 text-sm font-medium text-gray-900 dark:text-gray-400",
                    ),
                    Textarea(
                        id="message",
                        rows="6",
                        placeholder="Leave a comment...",
                        cls="block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg shadow-sm border border-gray-300 focus:ring-primary-500 focus:border-primary-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500",
                    ),
                    P(
                        "By submitting this form you agree to our",
                        A(
                            "terms and conditions",
                            href="#",
                            cls="text-primary-600 hover:underline dark:text-primary-500",
                        ),
                        "and our",
                        A(
                            "privacy policy",
                            href="#",
                            cls="text-primary-600 hover:underline dark:text-primary-500",
                        ),
                        "which explains how we may collect, use and disclose your personal information including to third parties.",
                        cls="mt-4 text-sm text-gray-500",
                    ),
                    cls="sm:col-span-2",
                ),
                Button(
                    "Send message",
                    type="submit",
                    cls="py-3 px-5 text-sm font-medium text-center text-white rounded-lg bg-primary-700 sm:w-fit hover:bg-primary-800 focus:ring-4 focus:outline-none focus:ring-primary-300 dark:bg-primary-600 dark:hover:bg-primary-700 dark:focus:ring-primary-800",
                ),
                action="#",
                cls="grid grid-cols-1 gap-8 p-6 mx-auto mb-16 max-w-screen-md bg-white rounded-lg border border-gray-200 shadow-sm lg:mb-28 dark:bg-gray-800 dark:border-gray-700 sm:grid-cols-2",
            ),
            Div(
                Div(
                    Div(
                        Svg(
                            Path(
                                d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z"
                            ),
                            Path(
                                d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z"
                            ),
                            fill="currentColor",
                            viewbox="0 0 20 20",
                            xmlns="http://www.w3.org/2000/svg",
                            cls="w-5 h-5 text-gray-600 lg:w-8 lg:h-8 dark:text-gray-500",
                        ),
                        cls="flex justify-center items-center mx-auto mb-4 w-10 h-10 bg-gray-100 rounded-lg dark:bg-gray-800 lg:h-16 lg:w-16",
                    ),
                    P("Email us:", cls="mb-2 text-xl font-bold dark:text-white"),
                    P(
                        "Email us for general queries, including marketing and partnership opportunities.",
                        cls="mb-3 text-gray-500 dark:text-gray-400",
                    ),
                    A(
                        "hello@supa_saas.com",
                        href="mailto:abc@example.com",
                        cls="font-semibold text-primary-600 dark:text-primary-500 hover:underline",
                    ),
                ),
                Div(
                    Div(
                        Svg(
                            Path(
                                d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"
                            ),
                            fill="currentColor",
                            viewbox="0 0 20 20",
                            xmlns="http://www.w3.org/2000/svg",
                            cls="w-5 h-5 text-gray-600 lg:w-8 lg:h-8 dark:text-gray-500",
                        ),
                        cls="flex justify-center items-center mx-auto mb-4 w-10 h-10 bg-gray-100 rounded-lg dark:bg-gray-800 lg:h-16 lg:w-16",
                    ),
                    P("Call us:", cls="mb-2 text-xl font-bold dark:text-white"),
                    P(
                        "Call us to speak to a member of our team. We are always happy to help.",
                        cls="mb-3 text-gray-500 dark:text-gray-400",
                    ),
                    Span(
                        "+1 (646) 786-5060",
                        cls="font-semibold text-primary-600 dark:text-primary-500",
                    ),
                ),
                Div(
                    Div(
                        Svg(
                            Path(
                                fill_rule="evenodd",
                                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-2 0c0 .993-.241 1.929-.668 2.754l-1.524-1.525a3.997 3.997 0 00.078-2.183l1.562-1.562C15.802 8.249 16 9.1 16 10zm-5.165 3.913l1.58 1.58A5.98 5.98 0 0110 16a5.976 5.976 0 01-2.516-.552l1.562-1.562a4.006 4.006 0 001.789.027zm-4.677-2.796a4.002 4.002 0 01-.041-2.08l-.08.08-1.53-1.533A5.98 5.98 0 004 10c0 .954.223 1.856.619 2.657l1.54-1.54zm1.088-6.45A5.974 5.974 0 0110 4c.954 0 1.856.223 2.657.619l-1.54 1.54a4.002 4.002 0 00-2.346.033L7.246 4.668zM12 10a2 2 0 11-4 0 2 2 0 014 0z",
                                clip_rule="evenodd",
                            ),
                            fill="currentColor",
                            viewbox="0 0 20 20",
                            xmlns="http://www.w3.org/2000/svg",
                            cls="w-5 h-5 text-gray-600 lg:w-8 lg:h-8 dark:text-gray-500",
                        ),
                        cls="flex justify-center items-center mx-auto mb-4 w-10 h-10 bg-gray-100 rounded-lg dark:bg-gray-800 lg:h-16 lg:w-16",
                    ),
                    P("Support", cls="mb-2 text-xl font-bold dark:text-white"),
                    P(
                        "Email us for general queries, including marketing and partnership opportunities.",
                        cls="mb-3 text-gray-500 dark:text-gray-400",
                    ),
                    A(
                        "Support center",
                        href="#",
                        cls="inline-flex py-2 px-4 text-sm font-medium text-center rounded-lg border text-primary-600 border-primary-600 hover:text-white hover:bg-primary-600 focus:ring-4 focus:outline-none focus:ring-primary-300 dark:border-primary-500 dark:text-primary-500 dark:hover:text-white dark:hover:bg-primary-600 dark:focus:ring-primary-800",
                    ),
                ),
                cls="space-y-8 text-center md:grid md:grid-cols-2 lg:grid-cols-3 md:gap-12 md:space-y-0",
            ),
            cls="py-16 px-4 mx-auto -mt-96 max-w-screen-xl sm:py-24 lg:px-6",
        ),
        cls="bg-white dark:bg-gray-900",
    )
