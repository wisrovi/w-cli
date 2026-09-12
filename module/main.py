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
# 23 live PyPI published packages + 14 development/internal modules = 37 total components
LIBRARY_MAPPING = {
    # Core Engine & Pipelines
    "pipe": ("wpipe", "High-performance Python pipeline orchestrator (Sync/Async)", "https://pypi.org/project/wpipe/"),
    "pipeline": ("wpipe", "High-performance Python pipeline orchestrator (Sync/Async)", "https://pypi.org/project/wpipe/"),
    "pipe-steps": ("wpipe-steps", "Official production-ready modular steps for wpipe", "https://pypi.org/project/wpipe-steps/"),
    "pipe-plugins": ("wpipe-plugins", "Community-driven plugin repository for custom steps", "https://pypi.org/project/wpipe-plugins/"),
    "pipe-mcp": ("wpipe-mcp", "FastMCP Server for wpipe pipeline architecture and verification", "https://pypi.org/project/wpipe-mcp/"),
    "pipe-api": ("wpipe-api", "FastAPI process monitoring backend API", "https://github.com/wisrovi/w-cli"),

    # Databases, Caching & Key-Value Stores
    "redis": ("wredis", "Redis sync/async integration & caching suite", "https://pypi.org/project/wredis/"),
    "redis-mcp": ("wredis-mcp", "FastMCP Server for Redis cache management and inspection", "https://pypi.org/project/wredis-mcp/"),
    "sqlite": ("wsqlite", "High-performance SQLite ORM wrapper with TableSync", "https://pypi.org/project/wsqlite/"),
    "sqlite-mcp": ("wsqlite-mcp", "FastMCP Server for SQLite database inspection and queries", "https://pypi.org/project/wsqlite-mcp/"),
    "postgresql": ("wpostgresql", "PostgreSQL connection pooler and enterprise ORM mapper", "https://pypi.org/project/wpostgresql/"),
    "postgresql-mcp": ("wpostgresql-mcp", "FastMCP Server for PostgreSQL AI agent integration", "https://pypi.org/project/wpostgresql-mcp/"),
    "wpostgresql-mcp": ("wpostgresql-mcp", "FastMCP Server for PostgreSQL AI agent integration", "https://pypi.org/project/wpostgresql-mcp/"),
    "wpostgresql_mcp": ("wpostgresql-mcp", "FastMCP Server for PostgreSQL AI agent integration", "https://pypi.org/project/wpostgresql-mcp/"),
    "clickhouse": ("wclickhouse", "ClickHouse ORM mapping using clickhouse-connect", "https://pypi.org/project/wclickhouse/"),
    "mongo": ("wmongo", "MongoDB document mapper utilizing Pydantic", "https://pypi.org/project/wmongo/"),
    "mysql": ("wmysql", "Pydantic ORM wrapper for MySQL", "https://github.com/wisrovi/w-cli"),
    "mariadb": ("wmariadb", "Pydantic ORM wrapper for MariaDB", "https://github.com/wisrovi/w-cli"),
    "elasticsearch": ("wElasticsearch", "Pydantic-based Elasticsearch document ORM", "https://github.com/wisrovi/w-cli"),
    "snowflake": ("wSnowflake", "Dynamic Snowflake SQL client ORM", "https://github.com/wisrovi/w-cli"),
    "databricks": ("wdatabricks", "Databricks SQL ORM framework", "https://github.com/wisrovi/w-cli"),

    # Messaging & Event Streaming
    "kafka": ("wkafka", "Decorator-based wrapper for Apache Kafka", "https://pypi.org/project/wkafka/"),
    "kafka-mcp": ("wkafka-mcp", "FastMCP Server for Kafka event streaming and topic inspection", "https://pypi.org/project/wkafka-mcp/"),
    "nats": ("wnats", "NATS message broker wrappers", "https://github.com/wisrovi/w-cli"),
    "zeromq": ("wzeroMQ", "IPC/TCP network sockets wrapper using ZeroMQ", "https://github.com/wisrovi/w-cli"),
    "messenger": ("wmessenger", "Telegram, WhatsApp, and Slack client API", "https://github.com/wisrovi/w-cli"),

    # Security & Zero Trust Cryptography
    "auth": ("wauth", "Machine-locked secrets encryption vault (AES-256 Fernet)", "https://pypi.org/project/wauth/"),
    "fabric": ("wFabricSecurity", "Zero Trust security system for Hyperledger Fabric", "https://pypi.org/project/wFabricSecurity/"),

    # MLOps, Computer Vision & Audio
    "yolo": ("wyolo", "MLflow and S3 YOLO/RT-DETR training workflow wrapper", "https://pypi.org/project/wyolo/"),
    "yolo-mcp": ("wyoloservice-mcp", "FastMCP Server for NeuralForgeAI YOLO cluster orchestration", "https://pypi.org/project/wyoloservice-mcp/"),
    "wyoloservice-mcp": ("wyoloservice-mcp", "FastMCP Server for NeuralForgeAI YOLO cluster orchestration", "https://pypi.org/project/wyoloservice-mcp/"),
    "audio": ("ProcessAudio", "Audio feature extraction and augmentation utility", "https://pypi.org/project/ProcessAudio/"),
    "agents": ("wAgents", "CUDA-enabled Docker development workspace for AI agents", "https://github.com/wisrovi/w-cli"),
    "image": ("wimage", "Image resizing and transformation library", "https://github.com/wisrovi/w-cli"),

    # Core Utilities, DevOps & Monorepo
    "container": ("wcontainer", "Docker SDK automation utility library", "https://pypi.org/project/wcontainer/"),
    "decorators": ("wdecorators", "Reusable high-level decorator collection", "https://pypi.org/project/wdecorators/"),
    "utils": ("wutils", "Common script scheduling and format checkers", "https://pypi.org/project/wutils/"),
    "wisrovi-python": ("wisrovi-python", "Core foundational Python utilities and algorithmic helpers", "https://pypi.org/project/wisrovi-python/"),
    "ticket": ("wticket", "Dynamic SLA helpdesk engine & remote license validator", "https://github.com/wisrovi/w-cli"),
    "wonka": ("wWonka", "Internal utilities helper library", "https://github.com/wisrovi/w-cli"),
    "haproxy": ("whaproxy", "HAProxy configuration compiler and controller", "https://github.com/wisrovi/w-cli"),
    "cli": ("w-cli", "Central CLI manager and package installer for the suite", "https://github.com/wisrovi/w-cli"),
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
        console.print(f"[bold red]Command failed for {package_name}:[/bold red] {e}")
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


def get_monorepo_root() -> str:
    """
    Traverse parent directories to locate the root monorepo or active workspace containing packages.
    """
    curr = os.path.abspath(os.getcwd())
    while curr != os.path.dirname(curr):
        if os.path.exists(os.path.join(curr, ".git")):
            return curr
        curr = os.path.dirname(curr)
    return os.path.abspath(os.getcwd())


def get_package_local_path(pkg_name: str) -> Optional[str]:
    """
    Resolve local path for a library within the monorepo workspace.
    """
    root = get_monorepo_root()
    candidate = os.path.join(root, pkg_name)
    if os.path.isdir(candidate):
        return candidate
    parent_candidate = os.path.join(os.path.dirname(root), pkg_name)
    if os.path.isdir(parent_candidate):
        return parent_candidate
    return None


@app.command(name="search")
def search(
    query: str = typer.Argument(..., help="Search query string matching name, shortname, or description")
):
    """
    Search registered wisrovi suite packages by keyword.
    """
    query_lower = query.lower()
    matches = []
    for short, (pkg, desc, url) in sorted(LIBRARY_MAPPING.items()):
        if query_lower in short.lower() or query_lower in pkg.lower() or query_lower in desc.lower():
            matches.append((short, pkg, desc, url))

    if not matches:
        console.print(f"[yellow]No matching library tags found for query '{query}'.[/yellow]")
        return

    table = Table(title=f"Search Results: '{query}' (Found {len(matches)})", show_header=True, header_style="bold green")
    table.add_column("Short Name", style="cyan", width=16)
    table.add_column("Package Name", style="green", width=18)
    table.add_column("Description", style="white")

    for short, pkg, desc, _ in matches:
        table.add_row(short, pkg, desc)

    console.print(table)


@app.command(name="check")
def check(
    library: str = typer.Argument("all", help="Target library to check or 'all'")
):
    """
    Execute Ruff syntax checking and Bandit security audits on local library repositories.
    """
    if library.lower() == "all":
        root = get_monorepo_root()
        dirs = [os.path.join(root, d) for d in os.listdir(root) if os.path.isdir(os.path.join(root, d))]
        valid_dirs = [d for d in dirs if os.path.exists(os.path.join(d, "pyproject.toml")) or os.path.exists(os.path.join(d, "setup.py"))]
        target_dirs = valid_dirs if valid_dirs else [root]
    else:
        target_dir = get_package_local_path(library) or os.getcwd()
        target_dirs = [target_dir]

    for d in target_dirs:
        console.print(f"\n[cyan]Auditing code quality in {d}...[/cyan]")
        try:
            subprocess.run(["ruff", "check", d], check=False)
            subprocess.run(["bandit", "-r", d, "-ll"], check=False)
        except Exception as e:
            console.print(f"[yellow]Linter execution note:[/yellow] {e}")


@app.command(name="link")
def link(
    library: str = typer.Argument(..., help="Library name to link in editable mode ('redis', 'all')")
):
    """
    Install local package in editable mode (-e) for development.
    """
    root = get_monorepo_root()

    if library.lower() == "all":
        candidates = []
        for d in os.listdir(root):
            path = os.path.join(root, d)
            if os.path.isdir(path) and (os.path.exists(os.path.join(path, "pyproject.toml")) or os.path.exists(os.path.join(path, "setup.py"))):
                candidates.append(path)

        console.print(f"[bold yellow]Found {len(candidates)} linkable local libraries.[/bold yellow]")
        for c in sorted(candidates):
            console.print(f"[cyan]>> Linking {os.path.basename(c)} in editable mode...[/cyan]")
            cmd = [sys.executable, "-m", "pip", "install", "-e", c]
            subprocess.run(cmd, check=False)
        return

    # Specific library
    target_dir = get_package_local_path(library)
    if not target_dir:
        pkg_name = LIBRARY_MAPPING.get(library.lower(), (library, "", ""))[0]
        target_dir = get_package_local_path(pkg_name) or os.path.join(root, pkg_name)

    cmd = [sys.executable, "-m", "pip", "install", "-e", target_dir]
    console.print(f"[bold blue]Linking package:[/bold blue] {' '.join(cmd)}")
    subprocess.run(cmd, check=False)
    console.print(f"[bold green]Successfully linked {library} in editable development mode.[/bold green]")


@app.command(name="sync-versions")
def sync_versions(
    version: str = typer.Argument(..., help="New semantic version string to synchronize across all packages")
):
    """
    Synchronize version field across all pyproject.toml files in the monorepo.
    """
    import tomli_w
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    root = get_monorepo_root()
    updated_count = 0

    for dirpath, _, filenames in os.walk(root):
        if "pyproject.toml" in filenames:
            toml_path = os.path.join(dirpath, "pyproject.toml")
            try:
                with open(toml_path, "rb") as f:
                    data = tomllib.load(f)
                if "project" in data and "version" in data["project"]:
                    data["project"]["version"] = version
                    with open(toml_path, "wb") as f:
                        tomli_w.dump(data, f)
                    updated_count += 1
                    console.print(f"[green]✓ Updated version to {version} in:[/green] {toml_path}")
            except Exception as e:
                console.print(f"[red]Error parsing {toml_path}:[/red] {e}")

    console.print(f"\n[bold green]Version synchronization complete. {updated_count} files updated to version {version}.[/bold green]")


@app.command(name="completion")
def completion():
    """
    Instructions to configure native shell auto-completion for 'w'.
    """
    console.print(Panel(
        "[bold cyan]Shell Auto-Completion Setup[/bold cyan]\n\n"
        "To enable tab-completion in bash or zsh, run:\n"
        "  [bold green]w --install-completion[/bold green]\n\n"
        "Or add to your shell config file (~/.bashrc or ~/.zshrc):\n"
        "  [dim]eval \"$(_W_COMPLETE=bash_source w)\"[/dim]",
        title="Shell Completion",
        expand=False
    ))


if __name__ == "__main__":
    app()
