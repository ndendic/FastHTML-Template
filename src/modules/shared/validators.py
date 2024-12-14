import re
from fasthtml.common import *
from monsterui.core import *
import json

def validate_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None


def validate_password(password):
    return len(password) >= 8


def priviledged_component(c, request, priviledge=None):
    user_privileges = request.session.get("priviledges", [])
    is_admin = json.loads(request.user).get("is_admin")
    if not is_admin:
        if priviledge not in user_privileges:
            return Div()
    return c
