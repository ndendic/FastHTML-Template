from typing import Type

from fasthtml.common import *
from fasthtml.core import APIRouter
from fasthtml.svg import *
from fh_frankenui import *
from fh_frankenui.core import *

from modules.shared.models import BaseTable
from modules.shared.templates import app_page, app_template, is_htmx


def InfoCard(title, value, change):
    return Div(Card(Div(H3(value), P(change, cls=TextFont.muted_sm)), header=H4(title)))


rev = InfoCard("Total Revenue", "$45,231.89", "+20.1% from last month")
sub = InfoCard("Subscriptions", "+2350", "+180.1% from last month")
sal = InfoCard("Sales", "+12,234", "+19% from last month")
act = InfoCard("Active Now", "+573", "+201 since last hour")

# %% ../example_dashboard.ipynb
top_info_row = Grid(rev, sub, sal, act, cols=4)


# %% ../example_dashboard.ipynb
def AvatarItem(name, email, amount):
    return Div(cls="flex items-center")(
        DiceBearAvatar(name, 9, 9),
        Div(cls="ml-4 space-y-1")(
            P(name, cls=TextFont.bold_sm), P(email, cls=TextFont.muted_sm)
        ),
        Div(amount, cls="ml-auto font-medium"),
    )


recent_sales = Card(
    Div(cls="space-y-8")(
        *[
            AvatarItem(n, e, d)
            for (n, e, d) in (
                ("Olivia Martin", "olivia.martin@email.com", "+$1,999.00"),
                ("Jackson Lee", "jackson.lee@email.com", "+$39.00"),
                ("Isabella Nguyen", "isabella.nguyen@email.com", "+$299.00"),
                ("William Kim", "will@email.com", "+$99.00"),
                ("Sofia Davis", "sofia.davis@email.com", "+$39.00"),
            )
        ]
    ),
    header=Div(
        H3("Recent Sales"), P("You made 265 sales this month.", cls=TextFont.muted_sm)
    ),
    cls="col-span-3",
)


# %% ../example_dashboard.ipynb
teams = [["Alicia Koch"], ["Acme Inc", "Monster Inc."], ["Create a Team"]]

opt_hdrs = ["Personal", "Team", ""]

team_dropdown = UkSelect(
    Optgroup(label="Personal Account")(Option(A("Alicia Koch"))),
    Optgroup(label="Teams")(Option(A("Acme Inc")), Option(A("Monster Inc."))),
    Option(A("Create a Team")),
)

rt = APIRouter()


@rt("/dashboard")
# @app_template("Dashboard", requieres="authenticated")
@app_template("Dashboard")
def page(request):
    return Div(cls="space-y-4")(
        H2("Dashboard"),
        TabContainer(
            Li(A("Overview", cls="uk-active")),
            Li(A("Analytics")),
            Li(A("Reports")),
            Li(A("Notifications")),
            uk_switcher="connect: #component-nav; animation: uk-animation-fade",
            alt=True,
        ),
        Ul(id="component-nav", cls="uk-switcher")(
            Li(
                top_info_row,
                Grid(
                    Card(H3("Overview to show here..."), cls="col-span-4"),
                    recent_sales,
                    gap=4,
                    cols=7,
                ),
                cls="space-y-4",
            ),
            Li(
                top_info_row,
                Grid(
                    Card(H3("Analytics to show here..."), cls="col-span-4"),
                    recent_sales,
                    gap=4,
                    cols=7,
                ),
                cls="space-y-4",
            ),
        ),
    )


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
