# FastHTML Template

A modern, feature-rich starter template for building web applications with FastHTML, TailwindCSS, and FH-FrankenUI.

## Features

- 🚀 Pre-configured FastHTML setup with hot-reload
- 💅 TailwindCSS and Flowbite integration for modern styling
- 📁 Clean and organized project structure
- 🛠️ Automated tools for development workflow
- 🔄 Automatic route collection system
- 📄 Built-in page creation script
- 🧪 Testing setup with pytest
- 🗃️ Built-in FastHTML database support
- 🔐 Complete authentication system

## Getting Started

This is a template repository on GitHub. To use it:

1. Click the "Use this template" button at the top of the repository
2. Create a new repository from this template
3. Clone your new repository:
```bash
git clone <your-new-repository-url>
cd <your-repository-name>
```

4. Initialize the development environment:
```bash
make init
```
This will:
- Create a virtual environment using `uv` (or standard venv if uv is not installed)
- Install all required dependencies
- Set up the project for development

5. Create your .env.example to include your prefered DATABASE_URL

6. Once in your virtual env start the project with:
```bash
make run
```
This will run example app on port 8000. You can change the port in main.py file.


## Project Structure

```
project/
├── app/                    # Application code
│   ├── components/         # Reusable UI components
│   ├── models/            # Data models
│   ├── pages/             # Page routes and views
│   ├── services/          # Business logic and services
│   │   └── db/           # Database services
│   ├── templates/         # Page templates
│   └── utils/            # Utility functions
├── config/                # Configuration files
├── static/                # Static assets
└── tests/                # Test files
```

## Automatic Route Collection

The template features an automatic route collection system that scans the `app/pages` directory and registers all routes automatically. Here's how it works:

1. Create a new page in the `app/pages` directory:
```python
# app/pages/hello.py
from fasthtml.common import *
from fasthtml.core import APIRouter

rt = APIRouter()

@rt("/hello")
def get(request):
    return "Hello, World!"
```

2. The route collector will automatically find and register this route - no manual registration needed!

You can create new pages by using:
```bash
make new-page ROUTE=your/page/path
```
This will create the same folder route structure under project/app/pages with routes attached to get and post methods.

```python
from fasthtml.common import *
from fasthtml.core import APIRouter

rt = APIRouter()

@rt("/your/page/path")
def get(request):
    return Titled("New Page", P("This is a new page"))

@rt("/your/page/path")
def post(request):
    # Handle POST request
    return {"message": "Received a POST request"}

# Add other HTTP methods as needed
```

## Database System

The template includes a database system built on SQLModel with a custom BaseTable class.

### Creating Models

Create new models by extending the BaseTable class:

```python
from sqlmodel import Field
from app.models.base import BaseTable

class Product(BaseTable, table=True):
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    description: str = Field(default="")
```

### Database Operations

The BaseTable class provides several convenient methods:

```python
# Create/Update
product = Product(name="Widget", price=9.99)
product.save()

# Query
all_products = Product.all()
specific_product = Product.get(product_id)

# Update
Product.update(product_id, {"price": 19.99})

# Delete
Product.delete(product_id)
```

### Database Migrations

The template uses Alembic for database migrations. If you're using SQLite, make sure you specify absolute database DATABSE_URL in your .env file.

1. After creating or modifying models, generate a migration:
```bash
alembic revision --autogenerate -m "Add product table"
```
or
```bash
make migrations
```


2. Apply the migration:
```bash
alembic upgrade head
```
or
```bash
make migrate
```
## Authentication System

The template includes a complete authentication system with the following features:

- User registration and login
- Password reset functionality 
- OAuth support - under development 🚧
- OTP (One-Time Password) support - emails are sent using Resend
- Session management

Example usage in a route:

```python
from app.services.auth import AuthService

auth = AuthService()

@rt("/login")
async def post(request):
    data = await request.json()
    user = await auth.login(request, data["email"], data["password"])
    if user:
        return {"status": "success"}
    return {"status": "error"}
```

## Development Commands

The project includes a Makefile with various helpful commands:

### Basic Commands

- `make run` - Start the FastHTML development server
- `make test` - Run all tests
- `make test-coverage` - Run tests with coverage report

### Page Management

Create a new page with automatic routing:
```bash
make new-page ROUTE=path/to/your/page
```

### Environment Management

- `make init` - Initialize development environment
- `make clean` - Clean up cache and temporary files

## Future Plans

- Default components for database table views
- Frontend rendering system for database records
- Enhanced authentication features
- More pre-built UI components

