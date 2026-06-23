import os
import sys
import subprocess
import webbrowser
from typing import Optional, List
import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Initialize typer app and rich console
app = typer.Typer(help="Wisrovi Libraries Suite Central CLI Manager")
console = Console()

# Unified mapping dictionary for the wisrovi suite libraries
# Format: short_name -> (official_package_name, description, doc_url)
LIBRARY_MAPPING = {
    "redis": ("wredis", "Redis sync/async integration & caching suite", "https://pypi.org/project/wredis/"),
    "sqlite": ("wsqlite", "High-performance SQLite ORM wrapper", "https://pypi.org/project/wsqlite/"),
    "clickhouse": ("wclickhouse", "ClickHouse ORM mapping using clickhouse-connect", "https://pypi.org/project/wclickhouse/"),
    "pipe": ("wpipe", "High-performance Python pipeline orchestrator", "https://wpipe.readthedocs.io/"),
    "pipeline": ("wpipe", "High-performance Python pipeline orchestrator", "https://wpipe.readthedocs.io/"),
    "auth": ("wauth", "Machine-locked secrets encryption vault", "https://pypi.org/project/wauth/"),
    "fabric": ("wFabricSecurity", "Zero Trust security system for Hyperledger Fabric", "https://wFabricSecurity.readthedocs.io/"),
    "audio": ("ProcessAudio", "Audio feature extraction and augmentation utility", "https://pypi.org/project/ProcessAudio/"),
    "yolo": ("wyolo", "MLflow and S3 YOLO/RT-DETR training workflow wrapper", "https://pypi.org/project/wyolo/"),
    "agents": ("wAgents", "Dev workspace for CUDA-enabled AI agents", "https://github.com/wisrovi/w-cli"),
    "elasticsearch": ("wElasticsearch", "Pydantic-based Elasticsearch document ORM", "https://github.com/wisrovi/w-cli"),
    "snowflake": ("wSnowflake", "Dynamic Snowflake SQL client ORM", "https://github.com/wisrovi/w-cli"),
    "wonka": ("wWonka", "Internal utilities helper library", "https://github.com/wisrovi/w-cli"),
    "container": ("wcontainer", "Docker SDK automation utility library", "https://pypi.org/project/wcontainer/"),
    "databricks": ("wdatabricks", "Databricks SQL ORM framework", "https://github.com/wisrovi/w-cli"),
    "decorators": ("wdecorators", "Reusable high-level decorator collection", "https://pypi.org/project/wdecorators/"),
    "haproxy": ("whaproxy", "HAProxy configuration compiler and controller", "https://github.com/wisrovi/w-cli"),
    "image": ("wimage", "Image resizing and transformation library", "https://github.com/wisrovi/w-cli"),
    "kafka": ("wkafka", "Decorator-based wrapper for Apache Kafka", "https://pypi.org/project/wkafka/"),
    "mariadb": ("wmariadb", "Pydantic ORM wrapper for MariaDB", "https://github.com/wisrovi/w-cli"),
    "messenger": ("wmessenger", "Telegram, WhatsApp, and Slack client API", "https://github.com/wisrovi/w-cli"),
    "mongo": ("wmongo", "MongoDB document mapper utilizing Pydantic", "https://pypi.org/project/wmongo/"),
    "mysql": ("wmysql", "Pydantic ORM wrapper for MySQL", "https://github.com/wisrovi/w-cli"),
    "nats": ("wnats", "NATS message broker wrappers", "https://github.com/wisrovi/w-cli"),
    "zeromq": ("wzeroMQ", "IPC/TCP network sockets wrapper using ZeroMQ", "https://github.com/wisrovi/w-cli"),
    "ticket": ("wticket", "Remote license/ticket validator suite", "https://pypi.org/project/wticket/"),
    "utils": ("wutils", "Common script scheduling and format checkers", "https://github.com/wisrovi/w-cli")
}


def detect_package_manager() -> str:
    """
    Detect which package manager is active in the current project directory.
    Returns: 'poetry', 'pipenv', or 'pip'.
    """
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "poetry.lock")) or os.path.exists(os.path.join(cwd, "poetry.toml")):
        return "poetry"
    if os.path.exists(os.path.join(cwd, "Pipfile")):
        return "pipenv"
    
    # Check parent directories for poetry config as fallback
    parent = os.path.dirname(cwd)
    while parent != cwd:
        if os.path.exists(os.path.join(parent, "poetry.lock")):
            return "poetry"
        cwd = parent
        parent = os.path.dirname(cwd)
        
    return "pip"


def run_install_command(package_name: str, manager: str) -> bool:
    """
    Run subprocess installation command based on detected manager.
    """
    if manager == "poetry":
        cmd = ["poetry", "add", package_name]
    elif manager == "pipenv":
        cmd = ["pipenv", "install", package_name]
    else:
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        
    console.print(f"[bold blue]Executing Command:[/bold blue] {' '.join(cmd)}")
    try:
        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]Installation failed for {package_name}:[/bold red] {e}")
        return False
    except FileNotFoundError:
        # Fallback to pip if poetry/pipenv binaries are not found in path
        console.print(f"[yellow]Manager '{manager}' binary not found. Falling back to pip...[/yellow]")
        cmd = [sys.executable, "-m", "pip", "install", package_name]
        try:
            result = subprocess.run(cmd, check=True)
            return result.returncode == 0
        except Exception as e:
            console.print(f"[bold red]Fallback installation failed:[/bold red] {e}")
            return False


@app.command(name="install")
def install(
    library: str = typer.Argument(..., help="Library name to install (e.g. 'redis', 'sqlite', 'all')"),
    manager_override: Optional[str] = typer.Option(None, "--manager", "-m", help="Force package manager ('pip', 'poetry', 'pipenv')")
):
    """
    Install libraries from the wisrovi suite.
    Maps short names directly to target packages (e.g., 'w install redis' -> installs 'wredis').
    """
    manager = manager_override if manager_override else detect_package_manager()
    console.print(f"[bold green]Package manager detected:[/bold green] {manager}")

    # Case 1: Install all libraries
    if library.lower() == "all":
        packages_to_install = list(set([data[0] for data in LIBRARY_MAPPING.values()]))
        console.print(f"[bold yellow]Installing all {len(packages_to_install)} libraries of the suite...[/bold yellow]")
        success_count = 0
        for pkg in sorted(packages_to_install):
            console.print(f"\n[cyan]>> Installing {pkg}...[/cyan]")
            if run_install_command(pkg, manager):
                success_count += 1
        console.print(f"\n[bold green]Installation completed: {success_count}/{len(packages_to_install)} packages installed successfully.[/bold green]")
        return

    # Case 2: Direct or shortname mapping
    normalized_lib = library.lower().strip()
    if normalized_lib in LIBRARY_MAPPING:
        package_name, description, _ = LIBRARY_MAPPING[normalized_lib]
        console.print(f"[green]Mapping '{library}' to wisrovi package:[/green] [bold cyan]{package_name}[/bold cyan] ({description})")
    else:
        # Fallback to direct library installation if not mapped
        package_name = library
        console.print(f"[yellow]'{library}' is not a registered short name. Attempting direct install...[/yellow]")

    if run_install_command(package_name, manager):
        console.print(f"[bold green]✓ Successfully installed {package_name}[/bold green]")
    else:
        console.print(f"[bold red]✗ Failed to install {package_name}[/bold red]")


@app.command(name="doc")
def doc(
    library: Optional[str] = typer.Argument(None, help="Library name to fetch docs for (e.g. 'pipe', 'redis')"),
    open_browser: bool = typer.Option(True, "--open/--no-open", help="Open documentation URL in web browser")
):
    """
    Open or show documentation details for wisrovi libraries.
    If no library is specified, prints the complete reference map.
    """
    if not library or library.lower() == "list":
        # Render a beautiful interactive table showing all options
        table = Table(title="Wisrovi Suite Packages Map", show_header=True, header_style="bold magenta")
        table.add_column("Short Name", style="cyan", width=15)
        table.add_column("Package Name", style="green", width=18)
        table.add_column("Description", style="white")
        table.add_column("Doc Endpoint", style="blue")

        for short, (pkg, desc, url) in sorted(LIBRARY_MAPPING.items()):
            table.add_row(short, pkg, desc, url)

        console.print(table)
        console.print("\n[bold yellow]Usage hint:[/bold yellow] Run 'w doc <short_name>' to open its docs.")
        return

    normalized_lib = library.lower().strip()
    if normalized_lib in LIBRARY_MAPPING:
        package_name, description, url = LIBRARY_MAPPING[normalized_lib]
        console.print(Panel(
            f"[bold green]Package:[/bold green] {package_name}\n"
            f"[bold green]Description:[/bold green] {description}\n"
            f"[bold green]Documentation:[/bold green] {url}",
            title=f"Documentation Ref: {normalized_lib}",
            expand=False
        ))
        
        if open_browser:
            console.print(f"[blue]Opening browser for:[/blue] {url}")
            webbrowser.open(url)
    else:
        console.print(f"[bold red]Error:[/bold red] '{library}' is not in the registered wisrovi mapping.")
        sys.exit(1)


@app.command(name="status")
def status():
    """
    Audit current python context environment.
    Identifies which wisrovi libraries are installed locally and displays their active versions.
    """
    # Fetch installed packages using importlib.metadata (Python 3.8+)
    try:
        from importlib.metadata import distributions
        installed_packages = {dist.metadata["Name"].lower(): dist.version for dist in distributions()}
    except ImportError:
        # Fallback to pkg_resources
        try:
            import pkg_resources
            installed_packages = {dist.key.lower(): dist.version for dist in pkg_resources.working_set}
        except ImportError:
            console.print("[bold red]Could not load packaging metadata engines.[/bold red]")
            sys.exit(1)

    table = Table(title="Local Environment wisrovi Packages Status", show_header=True, header_style="bold blue")
    table.add_column("Package Name", style="cyan", width=20)
    table.add_column("Description", style="white")
    table.add_column("Status", style="green", width=15)
    table.add_column("Version", style="yellow", width=12)

    unique_packages = sorted(list(set([data[0] for data in LIBRARY_MAPPING.values()])))

    for pkg in unique_packages:
        pkg_lower = pkg.lower()
        # Find matching short name description
        desc = "Wisrovi Suite Module"
        for short, (name, d, _) in LIBRARY_MAPPING.items():
            if name.lower() == pkg_lower:
                desc = d
                break

        if pkg_lower in installed_packages:
            table.add_row(pkg, desc, "Installed", installed_packages[pkg_lower])
        else:
            table.add_row(pkg, desc, "Not Installed", "-")

    console.print(table)


@app.command(name="create")
def create(
    template_type: str = typer.Argument(..., help="Template type to create ('pipeline' or 'docker-test')"),
    name: str = typer.Option("pipeline_sample", "--name", "-n", help="Target filename/project name to create")
):
    """
    Generate boilerplate templates matching monorepo and library standards.
    """
    cwd = os.getcwd()

    if template_type.lower() == "pipeline":
        filename = f"{name}.py" if not name.endswith(".py") else name
        filepath = os.path.join(cwd, filename)
        
        # WPipe basic pipeline structure boilerplate
        pipeline_template = """# -*- coding: utf-8 -*-
# wpipe boilerplate pipeline execution script
# Generated by 'w-cli create'

from wpipe import Pipeline, step

@step(name="extract_source_data", engine="thread", retries=3, delay=1.0)
def extract_source_data(context: dict) -> dict:
    \"\"\"
    Sample step to extract source information.
    \"\"\"
    print("Executing I/O bound extraction step...")
    return {"raw_data": [1, 2, 3, 4, 5], "status": "extracted"}

@step(name="transform_data", engine="process")
def transform_data(context: dict) -> dict:
    \"\"\"
    Sample process-bound step bypassing GIL.
    \"\"\"
    print("Executing CPU intensive transformation step...")
    raw = context.get("raw_data", [])
    squared = [x * x for x in raw]
    return {"processed_data": squared, "status": "transformed"}

def main():
    # Initialize pipeline with standard checkpoint storage
    p = Pipeline(pipeline_name="sample_orchestration_run")
    p.add_state(extract_source_data)
    p.add_state(transform_data)
    
    # Run the execution graph
    result = p.run({})
    print("Pipeline completed successfully. Result: ", result)

if __name__ == "__main__":
    main()
"""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(pipeline_template)
        console.print(f"[bold green]✓ Created pipeline boilerplate at:[/bold green] {filepath}")

    elif template_type.lower() == "docker-test":
        # 1. Create docker test runner shell script
        runner_path = os.path.join(cwd, "docker_test_runner.sh")
        runner_content = """#!/usr/bin/env bash
# docker_test_runner.sh
# Automate running Python tests inside a clean Docker container
# Generated by 'w-cli create'

set -euo pipefail

IMAGE_NAME="wisrovi/test-suite:latest"
WORKSPACE_DIR="$(pwd)"

echo "🐳 [1/3] Compiling test execution environment..."
docker build -t "${IMAGE_NAME}" -f - "${WORKSPACE_DIR}" <<EOF
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt pytest pytest-cov
COPY . .
EOF

echo "🧪 [2/3] Launching PyTest suite inside Docker container..."
docker run --rm \\
  -v "${WORKSPACE_DIR}/logs:/app/logs" \\
  -v "${WORKSPACE_DIR}/coverage_reports:/app/coverage_reports" \\
  "${IMAGE_NAME}" \\
  pytest --cov=module --cov-report=html:/app/coverage_reports/htmlcov --cov-report=term-missing

echo "📊 [3/3] Code Coverage assessment compiled successfully inside /coverage_reports/htmlcov/"
"""
        with open(runner_path, "w", encoding="utf-8") as f:
            f.write(runner_content)
        # Grant executable permissions
        os.chmod(runner_path, 0o755)
        
        # 2. Create sample test directory and test file
        test_dir = os.path.join(cwd, "test")
        os.makedirs(test_dir, exist_ok=True)
        
        test_file_path = os.path.join(test_dir, "test_sample.py")
        test_content = """# -*- coding: utf-8 -*-
# Unit test file matching pytest standards
# Generated by 'w-cli create'

import pytest

def test_arithmetic_assertion():
    \"\"\"
    Explicit test validating math base checks.
    Every test must have descriptive docstrings explaining its purpose.
    \"\"\"
    val = 10 * 10
    assert val == 100, "Math validation error"

def test_environment_context():
    \"\"\"
    Explicit test checking basic string mappings.
    \"\"\"
    test_str = "wisrovi"
    assert test_str.startswith("wis"), "Incorrect string prefix verification"
"""
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(test_content)
            
        console.print(f"[bold green]✓ Created Docker-Test environment boilerplate:[/bold green]")
        console.print(f"  - Runner script: {runner_path}")
        console.print(f"  - Test suite file: {test_file_path}")

    else:
        console.print(f"[bold red]Error:[/bold red] Unknown template type '{template_type}'. Supported: 'pipeline', 'docker-test'")
        sys.exit(1)


if __name__ == "__main__":
    app()
