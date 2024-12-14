from fasthtml.common import *
from datetime import datetime
from monsterui.core import *


class TableFieldRenderer:
    """Handles all field rendering logic for tables"""

    @staticmethod
    def render_header(field_info, col_name):
        title = (
            field_info.title
            if field_info and field_info.title
            else col_name.replace("_", " ").title()
        )
        if "icon" in field_info._attributes_set:
            icon = field_info._attributes_set.get("icon")
            if icon:
                return Th(
                    DivLAligned(
                        UkIcon(icon),
                        P(title),
                        cls="space-x-2",
                    )
                )
        return Th(title)

    @staticmethod
    def render_cell(field_info, value):
        def _Td(*args, cls="", **kwargs):
            return Td(*args, cls=f"p-2 {cls}", **kwargs)

        if not field_info:
            return _Td(value)

        input_type = field_info._attributes_set.get("input_type")
        if input_type:
            return TableFieldRenderer._render_by_input_type(input_type, value, _Td)

        return TableFieldRenderer._render_by_value_type(value, _Td)

    @staticmethod
    def _render_by_input_type(input_type, value, _Td):
        renderers = {
            "datetime": lambda v: _Td(
                v.strftime("%Y-%m-%d %H:%M:%S")
                if isinstance(v, datetime)
                else v
                if isinstance(v, str)
                else ""
            ),
            "checkbox": lambda v: _Td(CheckboxX(selected=v)),
            "email": lambda v: _Td(A(v, href=f"mailto:{v}")),
        }
        return renderers.get(input_type, lambda v: _Td(v))(value)

    @staticmethod
    def _render_by_value_type(value, _Td):
        if isinstance(value, datetime):
            return _Td(value.strftime("%Y-%m-%d %H:%M:%S"))
        elif isinstance(value, bool):
            return _Td(CheckboxX(checked=value, disabled=True))
        return _Td(value)
