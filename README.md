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
│   └── utils/             # Utility functions
├── config/                # Configuration files
├── static/                # Static assets
└── tests/                 # Test files
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

1. Define your models in the `app/models` directory
2. Use FastHTML's database API for queries and operations
3. Access the database through the FastHTML context in your routes

Example model:
```python
from fasthtml.db import Model, Column, String

class User(Model):
    name = Column(String)
    email = Column(String, unique=True)
```

Example usage in a route:
```python
@rt("/users")
def get(request):
    users = User.query.all()
    return Template("users.html", users=users)
```

## Contributing

1. Create a new branch for your feature
2. Make your changes
3. Run tests to ensure everything works
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
