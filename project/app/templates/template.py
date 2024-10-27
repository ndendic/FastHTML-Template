from fasthtml.common import *

def page(title, content):
    return Html(Head(Title(title)),Body(content))
