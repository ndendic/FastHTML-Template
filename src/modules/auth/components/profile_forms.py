"""FrankenUI Forms Example"""

import json

from fasthtml.common import *
from fasthtml.components import Uk_theme_switcher
from fasthtml.svg import *
from fh_frankenui.core import *

from modules.auth.models import User


def AvatarUploader(user_data):
    """Profile image uploader component with preview and click-to-upload"""
    if user_data:
        user = User.get(user_data["id"])
        current_avatar = (
            Img(
                src=user.avatar_url,
                cls="h-24 w-24 rounded-full object-cover cursor-pointer hover:opacity-80 transition-opacity",
                onclick="document.getElementById('avatar-input').click()",
            )
            if user.avatar_url
            else Div(
                DiceBearAvatar(user.full_name, 24, 24),
                cls="cursor-pointer hover:opacity-80 transition-opacity",
                onclick="document.getElementById('avatar-input').click()",
            )
        )
    else:
        current_avatar = DiceBearAvatar("Guest", 24, 24)

    return Card(
        Div(cls="space-y-4")(
            # Current avatar preview
            Div(cls="flex flex-col items-center gap-4")(
                current_avatar,
                P("Click avatar to change profile picture", cls=TextFont.muted_sm),
            ),
            # Upload form with preview
            Form(
                Input(
                    type="file",
                    name="avatar",
                    id="avatar-input",
                    accept="image/*",
                    cls="hidden",
                    onchange="this.form.requestSubmit()",
                ),
                hx_post="/upload-avatar",
                hx_target="#avatar-preview",
                hx_encoding="multipart/form-data",
            ),
            # Preview area
            Div(id="avatar-preview"),
        ),
        header=H3("Profile Picture"),
    )


def HelpText(c):
    return P(c, cls=TextFont.muted_sm)


def heading():
    return Div(cls="space-y-5")(
        H2("Settings"),
        P(
            "Manage your account settings and set e-mail preferences.",
            cls=TextFont.muted_lg,
        ),
        DividerSplit(),
    )


sidebar_items = ["Profile", "Appearance", "Account", "Notifications", "Display"]

sidebar = NavContainer(
    *map(lambda x: Li(A(x)), sidebar_items),
    uk_switcher="connect: #component-nav; animation: uk-animation-fade",
    cls=(NavT.secondary, "space-y-4 p-4 w-1/5"),
)


def profile_form(request):
    user_data = request.session.get("user")
    if user_data:
        user_data = json.loads(user_data)
        user = User.get(user_data["id"])

    content = Grid(
        # Avatar uploader
        Div(cls="col-span-2")(
            Div(cls="flex flex-col items-center")(
                # Avatar preview and upload will be handled by AvatarUploader component
                AvatarUploader(user_data),
            ),
        ),
        Div(cls="col-span-5")(
            Form(cls="space-y-6")(
                Div(cls="space-y-2")(
                    LabelInput(
                        "Full Name",
                        value=user.full_name,
                        placeholder="John Doe",
                        id="full_name",
                    ),
                    HelpText("Your full name will be displayed on your profile"),
                ),
                # Email
                Div(cls="space-y-2")(
                    LabelInput(
                        "Email",
                        value=user.email,
                        placeholder="john@example.com",
                        id="email",
                        type="email",
                    ),
                    HelpText("Your email address is used for login and notifications"),
                ),
                Button(cls=ButtonT.primary)(
                    "Save",
                    type="submit",
                    hx_post="/update-profile",
                    hx_swap="none",
                    # hx_swap_oob=True,
                    # hx_target="#table-container",
                ),
            ),
        ),
        gap=4,
        cols=7,
    )

    return UkFormSection(
        "Profile",
        "Manage your profile information and avatar",
        content,
        Form(
            hx_post="/update-profile",
            hx_target="#profile-form-result",
            hx_encoding="multipart/form-data",
        ),
        button_txt=None,
    )


def account_form():
    content = (
        Button(cls=ButtonT.primary)(
            "Refresh Products", hx_get="/subs/products", hx_swap="none"
        ),
        Div(cls="space-y-2")(
            LabelInput("Name", placeholder="Your name", id="name"),
            HelpText(
                "This is the name that will be displayed on your profile and in emails."
            ),
        ),
        Div(cls="space-y-2")(
            LabelInput(
                "Date of Birth",
                type="date",
                id="date_of_birth",
            ),
            HelpText("Your date of birth is used to calculate your age."),
        ),
        Div(cls="space-y-2")(
            LabelUkSelect(
                *Options(
                    "Select a language",
                    "English",
                    "French",
                    "German",
                    "Spanish",
                    "Portuguese",
                    selected_idx=1,
                    disabled_idxs={0},
                ),
                label="Language",
                id="language",
            ),
            HelpText("This is the language that will be used in the dashboard."),
        ),
    )

    return UkFormSection(
        "Account - Demo only",
        "Update your account settings. Set your preferred language and timezone.",
        button_txt="Update profile",
        *content,
    )


def appearance_form():
    content = (
        # Div(cls="space-y-2")(
        #     LabelUkSelect(
        #         *Options(
        #             "Select a font family",
        #             "Inter",
        #             "Geist",
        #             "Open Sans",
        #             selected_idx=2,
        #             disabled_idxs={0},
        #         ),
        #         label="Font Family",
        #         id="font_family",
        #     ),
        #     HelpText("Set the font you want to use in the dashboard."),
        # ),
        Div(cls="space-y-2")(
            # FormLabel("Theme"),
            # HelpText("Select the theme for the dashboard."),
            Uk_theme_switcher(),
        ),
    )

    return UkFormSection(
        "Appearance",
        "Customize the appearance of the app. Automatically switch between day and night themes.",
        # button_txt="Update preferences",
        button_txt=None,
        *content,
    )


def notifications_form():
    content = [
        Div(cls="space-y-2")(
            FormLabel("Notify me about"),
            *[
                Div(cls="space-x-2")(
                    Radio(
                        id=f"notification_{i}",
                        name="notification",
                        checked=(label == "Nothing"),
                    ),
                    FormLabel(label),
                )
                for i, label in enumerate(
                    ["All new messages", "Direct messages and mentions", "Nothing"]
                )
            ],
        ),
        Div(
            H3("Email Notifications", cls="mb-4 text-lg font-medium"),
            Div(cls="space-y-4")(
                *[
                    Div(
                        cls="flex items-center justify-between rounded-lg border border-border p-4"
                    )(
                        Div(cls="space-y-0.5")(
                            FormLabel(
                                item["title"],
                                cls="text-base font-medium",
                                for_=f"email_notification_{i}",
                            ),
                            HelpText(item["description"]),
                        ),
                        Toggle_switch(
                            checked=item["checked"], disabled=item["disabled"]
                        ),
                    )
                    for i, item in enumerate(
                        [
                            {
                                "title": "Communication emails",
                                "description": "Receive emails about your account activity.",
                                "checked": False,
                                "disabled": False,
                            },
                            {
                                "title": "Marketing emails",
                                "description": "Receive emails about new products, features, and more.",
                                "checked": False,
                                "disabled": False,
                            },
                            {
                                "title": "Social emails",
                                "description": "Receive emails for friend requests, follows, and more.",
                                "checked": True,
                                "disabled": False,
                            },
                            {
                                "title": "Security emails",
                                "description": "Receive emails about your account activity and security.",
                                "checked": True,
                                "disabled": True,
                            },
                        ]
                    )
                ]
            ),
        ),
        Div(cls="space-x-2")(
            CheckboxX(id="notification_mobile", checked=True),
            FormLabel(
                "Use different settings for my mobile devices", fr="notification_mobile"
            ),
        ),
        HelpText(
            "You can manage your mobile notifications in the mobile settings page."
        ),
    ]

    return UkFormSection(
        "Notifications - Demo only",
        "Configure how you receive notifications.",
        *content,
        button_txt="Update notifications",
    )


def display_form():
    content = Div(cls="space-y-2")(
        Div(cls="mb-4")(
            Span("Sidebar", cls="text-base font-medium"),
            HelpText("Select the items you want to display in the sidebar."),
        ),
        *[
            Div(CheckboxX(id=f"display_{i}", checked=i in [0, 1, 2]), FormLabel(label))
            for i, label in enumerate(
                ["Recents", "Home", "Applications", "Desktop", "Downloads", "Documents"]
            )
        ],
    )
    return UkFormSection(
        "Display - Demo only",
        "Turn items on or off to control what's displayed in the app.",
        button_txt="Update display",
        *content,
    )


def profile_page(request):
    return Div(cls="space-y-4")(
        H2("Account Settings"),
        TabContainer(
            *map(lambda x: Li(A(x)), sidebar_items),
            uk_switcher="connect: #component-nav; animation: uk-animation-fade",
            alt=True,
        ),
        Div(cls="flex gap-x-12")(
            Div(cls="flex-1")(
                Ul(id="component-nav", cls="uk-switcher")(
                    Li(cls="uk-active")(
                        profile_form(request),
                        Li()(appearance_form()),
                        Li()(account_form()),
                        Li()(notifications_form()),
                        Li()(display_form()),
                    )
                )
            ),
        ),
    )
