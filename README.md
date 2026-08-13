# 🧱 Wisrovi Libraries Suite CLI Launcher (`w-cli`)

A centralized CLI package manager, documentation lookup indexer, environment auditor, and development workspace helper for the **wisrovi Libraries Suite**.

Allows users to manage and install packages dynamically using simplified command interfaces (e.g. `w install redis` maps to installing `wredis` package on the system).

---

## 👨‍💻 Hecho por Wisrovi Rodríguez

Este repositorio y su conjunto de librerías son desarrollado y mantenido por **Wisrovi Rodríguez**. Todo el ecosistema de paquetes mostrado a continuación forma parte del portafolio corporativo de soluciones de código abierto y herramientas internas identificadas con la marca `wisrovi`.

---

## 📊 Complete Libraries Map (Mapa Corporativo de Librerías)

| Short Name | Package | Type | Registry / PyPI | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`pipe`** / **`pipeline`** | `wpipe` | Core Engine | [![PyPI](https://img.shields.io/pypi/dm/wpipe?color=green)](https://pepy.tech/projects/wpipe) | High-performance Python pipeline orchestrator (Sync/Async). |
| **`wpipe-steps`** | `wpipe-steps` | Core Extension | [![PyPI](https://img.shields.io/pypi/dm/wpipe-steps?color=green)](https://pepy.tech/projects/wpipe-steps) | Official, production-ready modular steps for the `wpipe` engine. |
| **`wpipe-plugins`** | `wpipe-plugins` | Core Extension | [![PyPI](https://img.shields.io/pypi/dm/wpipe-plugins?color=green)](https://pepy.tech/projects/wpipe-plugins) | Community-driven repository for custom steps and states. |
| **`wpipe-mcp`** | `wpipe-mcp` | Core Extension | [![PyPI](https://img.shields.io/pypi/dm/wpipe-mcp?color=green)](https://pepy.tech/projects/wpipe-mcp) | Model Context Protocol (MCP) server for pipeline design. |
| **`wpipe-api`** | `wpipe-api` | Core Extension | `Internal` | Process Monitor Backend API built with FastAPI. |
| **`ProcessAudio`** | `ProcessAudio` | MLOps / Audio | [![PyPI](https://img.shields.io/pypi/dm/ProcessAudio?color=green)](https://pepy.tech/projects/ProcessAudio) | Audio feature extraction and augmentation utility. |
| **`w-cli`** | `w-cli` | Utility CLI | `Development` | Central CLI launcher and indexer for the suite. |
| **`wAgents`** | `wAgents` | Dev Workspace | `Development` | CUDA-enabled Docker dev workspace for AI agents. |
| **`wElasticsearch`** | `wElasticsearch` | Database ORM | `Development` | Pydantic-based Elasticsearch document ORM. |
| **`wFabricSecurity`** | `wFabricSecurity` | Zero Trust Security | [![PyPI](https://img.shields.io/pypi/dm/wfabricsecurity?color=green)](https://pepy.tech/projects/wfabricsecurity) | Zero Trust security system for Hyperledger Fabric. |
| **`wSnowflake`** | `wSnowflake` | Database ORM | `Development` | Dynamic Snowflake SQL client ORM. |
| **`wWonka`** | `wWonka` | Utility Helpers | `Development` | Internal utilities helper library. |
| **`wauth`** | `wauth` | Security Vault | [![PyPI](https://img.shields.io/pypi/dm/wauth?color=green)](https://pepy.tech/projects/wauth) | Machine-locked secrets encryption vault. |
| **`wclickhouse`** | `wclickhouse` | Database ORM | [![PyPI](https://img.shields.io/pypi/dm/wclickhouse?color=green)](https://pepy.tech/projects/wclickhouse) | ClickHouse ORM mapping using clickhouse-connect. |
| **`wcontainer`** | `wcontainer` | DevOps Tool | [![PyPI](https://img.shields.io/pypi/dm/wcontainer?color=green)](https://pepy.tech/projects/wcontainer) | Docker SDK automation utility library. |
| **`wdatabricks`** | `wdatabricks` | Database ORM | `Development` | Databricks SQL ORM framework. |
| **`wdecorators`** | `wdecorators` | Code Utility | [![PyPI](https://img.shields.io/pypi/dm/wdecorators?color=green)](https://pepy.tech/projects/wdecorators) | Reusable high-level decorator collection. |
| **`whaproxy`** | `whaproxy` | DevOps Tool | `Development` | HAProxy configuration compiler and controller. |
| **`wimage`** | `wimage` | Code Utility | `Development` | Image resizing and transformation library. |
| **`wkafka`** | `wkafka` | Messaging | [![PyPI](https://img.shields.io/pypi/dm/wkafka?color=green)](https://pepy.tech/projects/wkafka) | Decorator-based wrapper for Apache Kafka. |
| **`wmariadb`** | `wmariadb` | Database ORM | `Development` | Pydantic ORM wrapper for MariaDB. |
| **`wmessenger`** | `wmessenger` | Messaging | `Development` | Telegram, WhatsApp, and Slack client API. |
| **`wmongo`** | `wmongo` | Database ORM | [![PyPI](https://img.shields.io/pypi/dm/wmongo?color=green)](https://pepy.tech/projects/wmongo) | MongoDB document mapper utilizing Pydantic. |
| **`wmysql`** | `wmysql` | Database ORM | `Development` | Pydantic ORM wrapper for MySQL. |
| **`wnats`** | `wnats` | Messaging | `Development` | NATS message broker wrappers. |
| **`wredis`** | `wredis` | Database ORM | [![PyPI](https://img.shields.io/pypi/dm/wredis?color=green)](https://pepy.tech/projects/wredis) | Redis sync/async integration & caching suite. |
| **`wsqlite`** | `wsqlite` | Database ORM | [![PyPI](https://img.shields.io/pypi/dm/wsqlite?color=green)](https://pepy.tech/projects/wsqlite) | High-performance SQLite ORM. |
| **`wticket`** | `wticket` | Remote API | `Development` | License validator using JSONBin.io backend. |
| **`wutils`** | `wutils` | Code Utility | `Development` | Common script scheduling and format checkers. |
| **`wyolo`** | `wyolo` | MLOps / Vision | [![PyPI](https://img.shields.io/pypi/dm/wyolo?color=green)](https://pepy.tech/projects/wyolo) | MLflow and S3 YOLO/RT-DETR training workflow. |
| **`wzeroMQ`** | `wzeroMQ` | Messaging | `Development` | IPC/TCP network sockets wrapper using ZeroMQ. |

**Total de librerías registradas:** 37

---

## 🚀 Installation & Local Setup

Install the CLI tool locally in editable mode to register the `w` script command on the shell path:

```bash
# Clone the repository
git clone https://github.com/wisrovi/w-cli.git
cd w-cli

# Install globally or to virtual environment in editable development mode
pip install -e .
```

---

## ⌨️ CLI Command Reference

Execute the `w` command to see all available subcommands:

### 1. Install Packages

Downloads and installs any package of the wisrovi suite. Automatically detects whether your active directory uses `pip`, `poetry`, or `pipenv` and runs the installation accordingly.

```bash
# Map and install wredis
w install redis

# Map and install wsqlite
w install sqlite

# Map and install wpipe
w install pipe

# Install ALL packages of the suite
w install all
```

### 2. Check Documentation

Retrieves PyPI documentation links and opens them in the default browser. If no package is specified, lists a table referencing all shortnames.

```bash
# List all libraries mappings
w doc

# Show reference card and open browser for wpipe documentation
w doc pipe

# Print info card without opening web browser
w doc redis --no-open
```

### 3. Check Package Status

Analyzes the active Python context path to audit which suite packages are installed locally.

```bash
w status
```

### 4. Create Boilerplates

Generates typical scripts or Docker testing environment wrappers matching project standards.

```bash
# Create a skeleton script for wpipe execution runs
w create pipeline --name my_pipeline

# Create docker testing runner script and unit test boilerplate file
w create docker-test
```

### 5. Link Local Packages (Editable Development Mode)

Finds the local subfolder path in your monorepo and links it dynamically to your virtual environment in editable mode. Extremely helpful to implement local changes immediately across projects.

```bash
# Link the local wredis package
w link redis

# Link ALL packages containing setup.py or pyproject.toml inside the monorepo root
w link all
```

### 6. Audit & Check Code Quality

Executes static syntax linting (`ruff`) and structural security code auditor scans (`bandit`) on specified local projects.

```bash
# Run audits on wredis directory
w check redis

# Audit all packages in the monorepo
w check all
```

### 7. Sync Version Tags

Iterates over all directories under the monorepo root containing `pyproject.toml` files and updates their version properties in block.

```bash
# Sincronizar todos los pyproject.toml de la suite a la versión 2.5.0
w sync-versions 2.5.0
```

### 8. Search Registered Packages

Performs clean matching searches inside shortnames, official names and descriptions.

```bash
# Search for packages related to 'database'
w search sqlite
```

### 9. Install Shell Completion

Enables native auto-completion of commands and package names in your shell environment.

```bash
# Register completion scripts inside active shell configs (~/.bashrc or ~/.zshrc)
w --install-completion
```

---

## 🧪 Unit Testing and Coverage

We implement automated static analysis and unit testing using `pytest`.

### Run Tests inside Docker (Isolated Environment)

Consistent with project testing rules, the test suite runs inside an isolated Docker container:

```bash
# Execute unit tests inside clean container context
./docker_test_runner.sh
```

### Run Coverage locally

Calculate code coverage metrics locally on development machines:

```bash
# Run tests and compile code coverage metrics report
./run_coverage.sh
```

HTML coverage results are written directly to `coverage_reports/htmlcov/index.html`.