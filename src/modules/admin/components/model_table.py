from fasthtml.common import *
from fasthtml.svg import *
from fh_frankenui.core import *
from fh_frankenui.foundations import stringify

from modules.admin.components.pagination import Pagination

from .renderers import TableFieldRenderer


def page_heading(model):
    return DivFullySpaced(cls="space-y-2")(
        Div(cls="space-y-2")(
            H2(model.display_name),
            P(
                f"Here's a list of your records in {model.display_name}",
                cls=TextFont.muted_sm,
            ),
        ),
    )


def table_controls(model, request):
    search_value = request.query_params.get("search_value", "")
    return DivFullySpaced(
        Form(
            Input(
                cls="w-[250px]",
                type="search",
                name="search_value",
                id="search_value",
                placeholder=f"Filter {model.display_name}",
                value=search_value,
                hx_get=f"/table/{model.__name__.lower()}/search",
                hx_trigger="keyup changed delay:500ms",
                hx_swap_oob=True,
                hx_target="#table-container",
            )
        ),
        Button(
            f"Create {model.display_name}",
            cls=(ButtonT.primary, TextFont.bold_sm),
            hx_get=f"/table/{model.__name__.lower()}/new",
            hx_target="#RecordData",
            hx_swap="outerHTML",
            uk_toggle="target: #RecordForm",
        ),
    )


def row_dropdown(record_id, table_name):
    return Td(cls="p-2")(
        Div(
            Button(UkIcon("ellipsis")),
            DropDownNavContainer(
                map(
                    NavCloseLi,
                    [
                        A(
                            "Edit",
                            uk_toggle="#RecordForm",
                            hx_get=f"/table/{table_name}/{record_id}",
                            hx_target="#RecordData",
                            hx_swap="outerHTML",
                        ),
                        A(
                            "Delete",
                            hx_delete=f"/table/{table_name}/{record_id}",
                            hx_confirm="Are you sure you want to delete this record?",
                            hx_target="#table-container",
                            hx_swap="innerHTML",
                        ),
                    ],
                )
            ),
        )
    )


def ModelTableFromDicts(
    header_data: Sequence,
    body_data: Sequence[dict],
    footer_data=None,
    model=None,
    header_cell_render=Th,
    cls=(TableT.middle, TableT.divider, TableT.hover, TableT.small),
    sortable=False,
    table_name="#",
    **kwargs,
):
    renderer = TableFieldRenderer()
    visible_headers = [h for h in header_data if h.lower() != "id"]
    return Table(
        Thead(
            Tr(
                *[
                    renderer.render_header(
                        model.model_fields.get(h) if model else None, h
                    )
                    for h in visible_headers
                ]
            )
        ),
        Tbody(
            *[
                Tr(
                    *[
                        renderer.render_cell(
                            model.model_fields.get(k) if model else None, r.get(k, "")
                        )
                        for k in visible_headers
                    ]
                    + [row_dropdown(r.get("id", ""), table_name)]
                )
                for r in body_data
            ],
            sortable=sortable,
        ),
        cls=stringify(cls),
        **kwargs,
    )


def ModelTable(model, request):
    page = int(request.query_params.get("page", 1))
    per_page = int(request.query_params.get("per_page", 10))
    table_data = model.table_view_data(request)
    total_records = len(table_data)
    total_table_records = model.total_records()
    total_pages = max(1, (total_table_records + per_page - 1) // per_page)

    pagination = Pagination(
        base_url=f"/table/{model.__name__.lower()}/search",
        current_page=page,
        total_pages=total_pages,
        per_page=per_page,
    )

    return Div(
        Div(
            cls="uk-overflow-auto mt-4 rounded-md border border-border",
            id="table-container",
        )(
            ModelTableFromDicts(
                header_data=model.table_view_fields,
                body_data=table_data,
                model=model,
                sortable=True,
                table_name=model.__name__.lower(),
            )
        ),
        pagination.__ft__(total_records, total_table_records),
    )


def table_ui(model, request):
    return Div(
        DivFullySpaced(cls="mt-8")(
            Div(cls="flex flex-1 gap-4")(table_controls(model, request))
        ),
        Div(id="table-container")(ModelTable(model, request)),
    )


def table_page(model, request):
    return Div(
        page_heading(model),
        table_ui(model, request),
        Modal(model(), id="RecordForm"),
    )
