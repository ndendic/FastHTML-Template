from fasthtml.common import *
from shad4fast import *  # Import Shad4Fast components

def hero():
    return Section(
            Div(
                Div(
                    # Title with Shad4Fast styling
                    H1(
                        "BOGI I TEODORAAAAA!!!!!",
                        cls="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl text-foreground",
                    ),
                    # Description with Shad4Fast muted styling
                    P(
                        "Bogi voli igicu, a Teodora voli Bogija. Svi vole Bogija i Teodoru.",
                        cls="leading-7 [&:not(:first-child)]:mt-6 text-muted-foreground",
                    ),
                    # Form with Shad4Fast components
                    Form(
                        Div(
                            Div(
                                # Label(
                                #     "Email address",
                                #     fr="member_email",
                                #     cls="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70",
                                # ),
                                # Using Shad4Fast Input component
                                Input(
                                    placeholder="Enter your email",
                                    type="email",
                                    name="member[email]",
                                    id="member_email",
                                    required="",
                                    cls="flex h-10 w-full md:w-96 rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
                                ),
                                # cls="relative w-auto mr-3",
                            # Using Shad4Fast Button component
                            Button(
                                "Try for free",
                                type="submit",
                                name="member_submit",
                                id="member_submit",
                                cls="inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
                            ),
                            cls="flex items-center mb-3 space-x-4",
                            ),

                        ),
                        Div(
                            "Instant signup. No credit card required. ",
                            Button(
                                "Terms of Service",
                                variant="link",
                                cls="px-0 text-primary",
                            ),
                            " and ",
                            Button(
                                "Privacy Policy",
                                variant="link",
                                cls="px-0 text-primary",
                            ),
                            ".",
                            cls="text-sm text-left text-muted-foreground",
                            
                        ),
                        action="#",
                        cls="space-y-4",
                    ),
                    cls="flex flex-col space-y-6 mr-auto place-self-center lg:col-span-7 xl:col-span-8",
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
            cls="bg-background border-b",
        )
