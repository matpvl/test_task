"""File containing invoke tasks used for development.

Not to be confused with the project1337.tasks which holds the Celery tasks.
"""

import os
import subprocess

import sys
from invoke import task
from re import compile as regex_compile
from re import escape as regex_escape
from re import IGNORECASE


MAIN_SRC_DIR = "src"


@task
def ruff(c):
    """Run ruff linter."""
    c.run("ruff check", pty=True)


@task
def ruff_format(c):
    """Format using ruff linter."""
    c.run("ruff format", pty=True)


@task
def mypy(c):
    """Run mypy type checks."""
    c.run("mypy .", pty=True)


@task
def black(c):
    """Run black to format code."""
    c.run("black .", pty=True)


@task
def radon_cc(c):
    """Run Radon to compute cyclomatic complexity."""
    c.run("radon cc . -a", pty=True)


@task
def radon_mi(c):
    """Run Radon to compute maintainability index."""
    c.run("radon mi .", pty=True)


@task
def tests(c):
    """Run tests."""
    c.run(f"pytest ./src/tests")


@task(pre=[black, ruff_format, mypy, ruff, radon_cc, radon_mi])
def lint(c):
    """Run all linters for code verification: ruff, mypy, radon."""
    print("All checks completed.")


@task(pre=[black, ruff_format, mypy, ruff, radon_cc, radon_mi, tests])
def build_local(c):
    """Run all tasks: mypy, black, and radon."""
    print("All checks completed.")


def determine_docker_command():
    """Try 'docker compose' first; fallback to 'docker-compose' if needed."""
    try:
        # Try 'docker compose' to see if it's available
        subprocess.run(
            ["docker", "compose", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return "docker compose"
    except subprocess.CalledProcessError:
        pass
    except FileNotFoundError:
        pass

    # Fallback to 'docker-compose'
    return "docker-compose"


@task
def buildup(c):
    """Build and run docker image."""
    docker_command = determine_docker_command()
    c.run(f"{docker_command} up --build", pty=True)


@task
def shell(c):
    """Run python shell for docker server instance."""
    docker_command = determine_docker_command()
    c.run(f"{docker_command} exec web poetry run python manage.py shell", pty=True)


@task
def server(c):
    """Run the server."""
    c.run("uvicorn main:app --port 8080")


@task
def todo(_c, name: str):
    """List all 'TODO' comments mentioning a specific name in the codebase."""
    print(f"Looking for 'TODO' comments mentioning {name} in the codebase...")
    print()

    # We search for matching 'TODO', optionally followed by any characters, then the specified name, case-insensitive
    pattern = regex_compile(
        r"\btodo\b.*?" + regex_compile(regex_escape(name), IGNORECASE).pattern,
        IGNORECASE,
    )

    comments_found = 0
    for root, _, files in os.walk(MAIN_SRC_DIR):
        for filename in files:
            if filename.endswith(".py"):
                with open(os.path.join(root, filename), "r", encoding="utf-8") as file:
                    content = file.read()
                    matches = pattern.finditer(content)
                    for match in matches:
                        line_start = content.rfind("\n", 0, match.start()) + 1
                        line_end = content.find("\n", match.end())
                        line_num = content.count("\n", 0, line_start) + 1
                        line_text = content[line_start:line_end].strip()

                        print(f"{root}/{filename}:{line_num}:")
                        print(line_text)
                        comments_found += 1

    print(f"Found {comments_found} 'TODO's mentioning {name} in the project files.")

    sys.stdout.flush()
