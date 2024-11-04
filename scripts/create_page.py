import os
import re
import sys


def create_page(route):
    # Convert route to file path
    file_path = f"project/app/pages/{route.strip('/')}.py"

    # Create directories if they don't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Check if file already exists
    if os.path.exists(file_path):
        print(f"Error: File already exists at {file_path}")
        return

    # Detect dynamic parameters
    params = re.findall(r"\[([^\]]+)\]", route)
    param_str = ", ".join(params)

    # Create boilerplate code
    boilerplate = f"""from fasthtml.common import *
from fasthtml.core import APIRouter

rt = APIRouter()

@rt("/{route.strip('/')}")
def get(request{', ' + param_str if params else ''}):
    return Titled("New Page", P("This is a new page{' for ' + ' and '.join(params) if params else ''}"))

@rt("/{route.strip('/')}")
def post(request{', ' + param_str if params else ''}):
    # Handle POST request
    return {{"message": "Received a POST request{' for ' + ' and '.join(params) if params else ''}"}}

# Add other HTTP methods as needed
"""

    # Write boilerplate to file
    with open(file_path, "w") as f:
        f.write(boilerplate)

    print(f"Created new page at {file_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python create_page.py <route>")
        sys.exit(1)

    create_page(sys.argv[1])
