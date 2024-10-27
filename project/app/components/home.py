from fasthtml.common import *
from .app_navbar import app_navbar
import json


def home(user):
    json_object = json.loads(user)
    email = json_object["email"]
    return Div(
        app_navbar(),
        Main(
            H2(
                f"Welcome to {email}'s Dashboard",
                cls="text-4xl font-extrabold dark:text-white",
            ),
            Div(
                Div(
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-48"
                    ),
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-48"
                    ),
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-48"
                    ),
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-48"
                    ),
                    cls="col-span-1 grid gap-4 mb-4 lg:mb-0",
                ),
                Div(
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-64"
                    ),
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-64"
                    ),
                    Div(
                        cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex items-center justify-center h-32 lg:h-64"
                    ),
                    cls="col-span-2 flex flex-col gap-4",
                ),
                cls="grid grid-cols-1 lg:grid-cols-3 gap-0 lg:gap-4",
            ),
            Div(
                Div(
                    cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex-1 flex items-center justify-center w-full h-32 lg:h-64"
                ),
                Div(
                    cls="border-2 border-dashed border-gray-200 rounded-xl dark:border-gray-600 flex-1 flex items-center justify-center w-full h-32 lg:h-64"
                ),
                cls="grid gap-4",
            ),
            cls="flex-1 p-4 space-y-4",
        ),
        cls="antialiased bg-white dark:bg-gray-900",
    )
