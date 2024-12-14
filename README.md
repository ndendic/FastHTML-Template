# FastHTML Template

A modern, feature-rich starter template for building web applications with FastHTML, TailwindCSS, and FH-FrankenUI.

## Features

- 🚀 Pre-configured FastHTML setup with hot-reload
- 💅 MonsterUI for modern styling
- 📁 Clean and organized project structure
- 🛠️ Automated tools for development workflow
- 🔄 Automatic route collection system
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
This project uses ```uv``` as package manager. 
```bash
uc sync
uv pip install -e . # to use local cli
```
This will:
- Create a virtual environment using `uv` (or standard venv if uv is not installed)
- Install all required dependencies
- Set up the project for development

5. Create your .env based on .env.example to include your prefered DATABASE_URL

6. Once in your virtual env start the project with:
```bash
fh run
```
This will run example app on port 8000. You can change the port in main.py file.


## Project Structure

```
project/
├── src/ # Application code
│ ├── modules/ # Feature modules
│ │ ├── admin/ # Admin module
│ │ │ └── components/
│ │ ├── auth/ # Authentication module
│ │ │ ├── components/
│ │ │ └── routes/
│ │ ├── public/ # Public pages module
│ │ │ ├── components/
│ │ │ └── routes/
│ │ └── shared/ # Shared code
│ │ ├── libs/
│ │ ├── templates/
│ │ └── validators/
│ └── assets/ # Static assets
└── config/ # Configuration files
```

## Automatic Route Collection

The template features an automatic route collection system that scans the modules for `rt` APIRouters and registers all routes automatically. Here's how it works:

1. Create a new page in the under your module `src/modules/your_module` directory:
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
fh migrations
```


2. Apply the migration:
```bash
alembic upgrade head
```
or
```bash
fh migrate
```
## Authentication System

The template includes a complete authentication system with the following features:

- User registration and login
- Password reset functionality 
- OAuth support - under development 🚧
- OTP (One-Time Password) support - emails are sent using Resend
- Session management


## Development Commands

The project includes it's own mini CLI with various helpful commands:

### Basic Commands

- `fh run` - Start the FastHTML development server
- `fh migrations` - Create DB migrations
- `fh migrate` - Migrates changes to db DB

### Page Management

## Future Plans

- Default components for database table views
- Frontend rendering system for database records
- Enhanced authentication features
- More pre-built UI components

