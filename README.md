# FastHTML Template

A modern, feature-rich starter template for building web applications with FastHTML, TailwindCSS, and Flowbite.

## Features

- 🚀 Pre-configured FastHTML setup with hot-reload
- 💅 TailwindCSS and Flowbite integration for modern styling
- 📁 Clean and organized project structure
- 🛠️ Automated tools for development workflow
- 🔄 Automatic route collection system
- 📄 Built-in page creation script
- 🧪 Testing setup with pytest
- 🗃️ Built-in FastHTML database support

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd FastHTML-Template
```

2. Initialize the development environment:
```bash
make init
```
This will:
- Create a virtual environment using `uv` (or standard venv if uv is not installed)
- Install all required dependencies
- Set up the project for development

## Codebase Structure

### Top-Level Overview

```
FastHTML-Template/
├── docs/                  # Documentation files
├── notebooks/             # Jupyter Notebooks for testing and documentation
│   ├── FastHTML.ipynb     # Example notebook
│   └── .ipynb_checkpoints/ # Notebook checkpoints
├── project/               # Main project directory
├── scripts/               # Utility scripts
│   ├── create_page.py     # Script to create new pages
│   └── post_template_setup.py # Script to set up the template
├── .gitignore             # Git ignore file
├── Makefile               # Makefile with various commands
├── pyproject.toml         # Project configuration file
└── README.md              # Project README file
```

### Project structure
```project/
├── app/                    # Application code
│   ├── components/         # Reusable UI components
│   │   ├── landing/        # Landing page components
│   │   │   ├── footer.py
│   │   │   ├── hero.py
│   │   │   ├── navbar.py
│   │   │   └── page.py
│   │   └── application/    # Application-specific components
│   │       └── navbar.py
│   ├── models/             # Data models
│   │   └── base.py
│   ├── pages/              # Page routes and views
│   │   ├── application/    # Application-specific pages
│   │   ├── err/            # Error pages
│   │   ├── templates/      # Page templates
│   │   │   ├── __init__.py
│   │   │   └── template.py
│   │   ├── about.py        # About page
│   │   ├── index.py        # Home page
│   │   └── pricing.py      # Pricing page
│   ├── services/           # Business logic and services
│   │   └── db/             # Database services
│   ├── templates/          # Page templates
│   └── utils/              # Utility functions
├── config/                 # Configuration files
├── static/                 # Static assets
└── tests/                  # Test files
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
Example:
```bash
make new-page ROUTE=users/[id]/profile
```
This will create a new page with both GET and POST handlers at `app/pages/users/[id]/profile.py`

### Environment Management

- `make init` - Initialize development environment
- `make clean` - Clean up cache and temporary files

### GitHub Integration

Initialize and push to GitHub:
```bash
make github-init REPO=your-repo-name
```

## Usage Examples

1. Create a new page:
```bash
make new-page ROUTE=blog/[post_id]
```

2. Start the development server:
```bash
make run
```

3. Run tests:
```bash
make test
```

## Database Usage

The template uses FastHTML's built-in database functionality. To work with the database:

1. Define your models by extending the `BaseTable` class in the `app/models` directory.
2. Use FastHTML's database API for queries and operations.
3. Access the database through the FastHTML context in your routes.

### BaseTable Features

The `BaseTable` class provides the following features:
- Automatic UUID primary key generation.
- Timestamps for creation and updates.
- Common database operations such as `query`, `get`, `update`, `delete`, and `upsert`.
- Custom dictionary serialization with support for nested models and datetime fields.

Example model:
```python
from datetime import datetime
from typing import Any, Dict, Optional
from sqlmodel import Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSON
from app.models.base import BaseTable

class User(BaseTable, table=True):
    email: str = Field(nullable=False)
    password: str = Field(default="")
    role: str = Field(default="authenticated")
    is_admin: bool = Field(default=False)
    user_metadata: Dict[str, Any] = Field(sa_column=Column(JSON))
    confirmed_at: Optional[datetime] = None
    email_confirmed_at: Optional[datetime] = None
    last_sign_in_at: Optional[datetime] = None

    table_fields = ["id", "email", "first_name", "last_name", "is_admin"]

    @classmethod
    def get_by_email(cls, email: str) -> "User":
        return cls.get(id=email, alt_key="email")
```


## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
