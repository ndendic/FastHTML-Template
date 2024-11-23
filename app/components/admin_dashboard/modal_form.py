from fasthtml.common import *
from fh_frankenui.core import *


class ModalForm:
    def __init__(self, record):
        self.rec = record
        self.form_data = record.form_data()

    def render_field(self, field: dict) -> str:
        field_type = field.get("type", "text")
        title = field["title"] if field["title"] else field["name"]
        if field["name"] == "id":
            return None

        if field_type in ["text", "email"]:
            return LabelInput(title, value=field.get("value", ""), id=field["name"])

        elif field_type == "checkbox":
            return LabelSwitch(
                name=field["name"],
                label=title,
                checked=field.get("value", False),
            )

        elif field_type == "json":
            return TextArea(
                name=field["name"],
                label=title,
                value=str(field.get("value", "")),
                rows=4,
            )
        elif field_type == "select":
            # Get options from schema_extra if available
            options = []
            if "options" in field:
                options = field["options"]

            return LabelSelect(
                *[Option(opt["label"], value=opt["value"]) for opt in options],
                name=field["name"],
                label=title,
                value=field.get("value", ""),
                required=field.get("required", False),
            )
        # Default to text input
        return LabelInput(name=field["name"], label=title, value=field.get("value", ""))

    def __ft__(self) -> FT:
        form_content = []

        # Handle grouped fields
        if self.form_data.get("groups"):
            for group in self.form_data["groups"]:
                form_content.append(
                    Div(cls="space-y-4")(
                        H4(group["name"], class_="text-lg font-medium mb-4"),
                        Div(
                            *[self.render_field(field) for field in group["fields"]],
                            class_="space-y-4",
                        ),
                    )
                )
                form_content.append(
                    Input(
                        name="id",
                        type="hidden",
                        value=self.form_data.get("id", ""),
                    )
                )
        # Handle ungrouped fields
        elif self.form_data.get("fields"):
            form_content.append(
                Div(cls="space-y-4")(
                    *[self.render_field(field) for field in self.form_data["fields"]],
                )
            )
            form_content.append(
                Input(
                    name="id",
                    type="hidden",
                    value=self.form_data.get("id", ""),
                )
            )

        is_new = not self.rec.inserted()

        modal_content = Div(cls="p-6")(
            H2(f"{'Create' if is_new else 'Edit'} {self.rec.display_name}"),
            P(
                f"Fill out the information below to {'create a new' if is_new else 'edit the'} record",
                cls=TextFont.muted_sm,
            ),
            Br(),
            Form(cls="space-y-6")(
                *form_content,
                DivRAligned(
                    ModalCloseButton("Cancel", cls=ButtonT.ghost),
                    ModalCloseButton(cls=ButtonT.primary)(
                        "Submit",
                        type="submit",
                        hx_post=f"/table/{self.rec.__class__.__name__.lower()}/upsert",
                        hx_swap_oob=True,
                        hx_target="#table-container",
                    ),
                    cls="space-x-5",
                ),
            ),
            id="RecordData",
        )

        return modal_content
