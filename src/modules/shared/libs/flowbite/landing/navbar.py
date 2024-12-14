from fasthtml.common import *
from shad4fast import *
from lucide_fasthtml import Lucide

def ThemeToggle(variant="ghost", cls=None, **kwargs):
    return Button(
        Lucide("sun", cls="dark:flex hidden"),
        Lucide("moon", cls="dark:hidden"),
        variant=variant,
        size="icon",
        cls=f"theme-toggle {cls}",
        **kwargs,
    )

def MobileMenu():
    return Sheet(
        SheetTrigger(
            Lucide(
                "menu",
                cls="size-7 fixed top-5 right-5 z-50 md:hidden cursor-pointer hover:opacity-75 transition-opacity",
                data_ref="sheet-trigger",
            ),
            cls="size-4 fixed top-4 right-4 z-50 md:hidden cursor-pointer",
            variant="ghost",
        ),
        SheetContent(

            # Navigation Links
            Div(
                A("Home", href="/", cls="block py-2"),
                A("About", href="/about", cls="block py-2"),
                A("Contact", href="/contact", cls="block py-2"),
                
                cls="flex flex-col h-[calc(100vh-12rem)]"
            ),
            SheetFooter(
                Button("Login/Register", variant="default", cls="w-full"),
                Separator(cls="my-4"),                
                ThemeToggle(cls="w-full mt-4"),

                # Button("Register", variant="default", cls="w-full mt-2"),
            ),
            side="left",  # Changed from left to right
            cls="w-[280px] sm:w-[400px]"
        ),
        standard=True
    )

def Navbar():
    return Div(
        Header(
            Div(
                # Logo/Brand (Left side)
                A(
                    H1("FastSaas", cls="text-xl font-bold"),
                    href="/",
                    cls="hover:opacity-75 transition-opacity"
                ),
                
                # Right side items
                Div(
                    # Desktop Navigation Links
                    Nav(
                        A("Home", href="/", cls="hover:underline"),
                        A("About", href="/about", cls="hover:underline"),
                        A("Contact", href="/contact", cls="hover:underline"),
                        cls="hidden md:flex items-center space-x-6"
                    ),               
                    # Auth buttons and toggles
                    Div(
                        ThemeToggle(cls="hidden md:inline-flex"),
                        A(
                            Button(
                                "Login",
                                variant="default",
                                cls="hidden md:inline-flex"
                            ),
                            href="/auth/login",
                        ),
                        cls="flex items-center space-x-4"
                    ),
                    cls="flex items-center space-x-6"
                ),
                cls="container flex items-center justify-between h-16"
            ),
            cls="fixed top-0 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60"
        ),
        MobileMenu(),
        cls="flex flex-col"
    )
