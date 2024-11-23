from fasthtml.common import *
from app.services.auth.auth_service import AuthService
from fasthtml.core import APIRouter
from typing import Type
from ..templates import app_page, is_htmx
from app.models import BaseTable

auth_service = AuthService()

rt = APIRouter()


def find_base_table_class(table_name: str) -> Type[BaseTable]:
    for subclass in BaseTable.__subclasses__():
        if subclass.__name__.lower() == table_name.lower():
            return subclass
    return None


@rt("/table/{table}")
def get(request, table: str = ""):
    if table:
        model: BaseTable = find_base_table_class(table)
        if model:
            if is_htmx(request):
                return model.render_table(request)
            else:
                return app_page("Table", request, model.render_table(request))
        else:
            return Div(f"Model {table} not found.")
    else:
        return H1("Table not found")


@rt("/table/{table}/search")
def get(request, table: str = ""):
    model: BaseTable = find_base_table_class(table)
    if model:
        return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")


@rt("/table/{table}/{record_id}")
def get(request, table: str = "", record_id: str = ""):
    model_class = find_base_table_class(table)
    if model_class:
        if record_id == "new":
            return model_class()
        else:
            record = model_class.get(record_id)
            if record:
                return record
            else:
                return H1("Record not found")
    else:
        return H1("Table not found")


@rt("/table/{table}/upsert")
async def post(request, table: str = ""):
    model: BaseTable = find_base_table_class(table)
    form_data = await request.form()
    processed_data = dict(form_data)

    for key, value in processed_data.items():
        if value == "on":  # If it's a checkbox value
            processed_data[key] = True
        elif value == "":  # If checkbox is unchecked, it won't be in form data
            processed_data[key] = False

    if model:
        if model.upsert(processed_data):
            return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")


@rt("/table/{table}/{record_id}")
def delete(request, table: str = "", record_id: str = ""):
    model: BaseTable = find_base_table_class(table)
    if model:
        model.delete_record(record_id)
        return model.render_table(request, records_only=True)
    else:
        return H1("Table not found")
