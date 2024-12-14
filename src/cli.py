import os
from enum import StrEnum
import typer
from rich import print
import subprocess

app = typer.Typer(name="FH Template Helper")


@app.command()
def init():
    """
    Initialize the development environment using uv or venv.
    """
    print("[yellow]Checking if uv is installed...[/yellow]")
    try:
        # Check if uv is installed
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("[green]uv is installed. Creating new environment...[/green]")
        
        # Create and activate environment using uv
        subprocess.run(["uv", "sync"], check=True)
        print("[green]Dependencies installed successfully![/green]")
        
    except subprocess.CalledProcessError:
        # If uv is not installed, offer choice
        print("[yellow]uv is not installed. Would you like to:[/yellow]")
        print("1) Install uv (recommended)")
        print("2) Continue with standard venv")
        
        choice = typer.prompt("Enter choice", type=int, default=1)
        
        if choice == 1:
            print("[yellow]Installing uv...[/yellow]")
            # Install uv using curl
            subprocess.run(
                ["curl", "-LsSf", "https://astral.sh/uv/install.sh"],
                stdout=subprocess.PIPE,
                check=True
            )
            subprocess.run(["uv", "venv", ".venv"], check=True)
            subprocess.run([".venv/bin/uv", "pip", "install", "-e", "."], check=True)
        else:
            print("[yellow]Creating standard venv environment...[/yellow]")
            subprocess.run(["python", "-m", "venv", ".venv"], check=True)
            subprocess.run([".venv/bin/pip", "install", "-e", "."], check=True)
        
        print("[green]Environment created and dependencies installed![/green]")

@app.command()
def migrations(message: str = typer.Option("Pushing changes", help="Optional migration message")):
    """
    Automate Alembic migration generation.
    """
    print(f"Generating Alembic migration with message: {message}")
    try:
        # alembic revision --autogenerate -m "Pushing changes"
        subprocess.run(["alembic", "revision", "--autogenerate", "-m", message], check=True)
        print("[green]Migration created successfully![/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]Error running Alembic: {e}[/red]")

@app.command()
def migrate():
    """
    Apply all pending Alembic migrations.
    """
    print("[yellow]Applying database migrations...[/yellow]")
    try:
        subprocess.run(["alembic", "upgrade", "head"], check=True)
        print("[green]Migrations applied successfully![/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]Error applying migrations: {e}[/red]")

@app.command()
def run():
    """
    Run the FastHTML application.
    """
    print("[yellow]Starting FastHTML application...[/yellow]")
    try:
        subprocess.run(["python", "src/main.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[red]Error starting application: {e}[/red]")

@app.command()
def test():
    """
    Run all tests.
    """
    print("[yellow]Running tests...[/yellow]")
    try:
        subprocess.run(["pytest", "tests/", "-v"], check=True)
        print("[green]Tests completed successfully![/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]Error running tests: {e}[/red]")

@app.command()
def test_coverage():
    """
    Run tests with coverage report.
    """
    print("[yellow]Running tests with coverage report...[/yellow]")
    try:
        subprocess.run([
            "pytest",
            "tests/",
            "--cov=src",
            "--cov-report=html",
            "--cov-report=term-missing"
        ], check=True)
        print("[green]Coverage report generated successfully![/green]")
    except subprocess.CalledProcessError as e:
        print(f"[red]Error generating coverage report: {e}[/red]")


if __name__ == "__main__":
    app()