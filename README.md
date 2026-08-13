# 🧱 Wisrovi Libraries Suite CLI Launcher (`w-cli`)

A centralized CLI package manager, documentation lookup indexer, environment auditor, and development workspace helper for the **wisrovi Libraries Suite**.

Allows users to manage and install packages dynamically using simplified command interfaces (e.g. `w install redis` maps to installing `wredis` package on the system).

---

## 📊 Complete Libraries Map

| Library / Component | Type | Registry / PyPI Status | Description | Key Details & Technical Features |
| :--- | :--- | :--- | :--- | :--- |
| **`wpipe`** | Core Engine | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wpipe?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wpipe) | High-performance Python pipeline orchestrator (Sync/Async). | WAL-mode SQLite state storage, GIL bypass, DAG scheduling, dynamic checkpointing. |
| **`wpipe-steps`** | Core Extension | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wpipe-steps?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wpipe-steps)  | Official, production-ready modular steps for the `wpipe` engine. | Packs for DBs (Redis, MySQL, Clickhouse), SFTP, security scanner, Telegram/Slack integration. |
| **`wpipe-plugins`** | Core Extension | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wpipe-plugins?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wpipe-plugins)  | Community-driven repository for custom steps and states. | Autocataloging parser (`steps_catalog.json`), Pydantic input validation structures. |
| **`wpipe-mcp`** | Core Extension | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wpipe-mcp?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wpipe-mcp)  | Model Context Protocol (MCP) server for pipeline design. | Local stdio/SSE execution, guides LLMs to generate valid structures (DTO, states, main). |
| **`wpipe-api`** | Core Extension | `Internal` | Process Monitor Backend API built with FastAPI. | Worker processes tracking, active state health checks, dashboard endpoints. |
| **`ProcessAudio`** | MLOps / Audio | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/ProcessAudio?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/ProcessAudio) | Audio feature extraction and augmentation utility. | Waveform rendering, audio stretching, and background noise injectors. |
| **`w-cli`** | Utility CLI | `Development` | Central CLI launcher and indexer for the suite. | Automates building, path discovery, and cross-package version indexing. |
| **`wAgents`** | Dev Workspace | `Development` | CUDA-enabled Docker dev workspace for AI agents. | NVIDIA CUDA 12.0, pre-configured Ruff linting, S3 DVC client, Bandit security scanner. |
| **`wElasticsearch`** | Database ORM | `Development` | Pydantic-based Elasticsearch document ORM. | Type-safe document operations, dynamic index mappings, bulk indexes. |
| **`wFabricSecurity`** | Zero Trust Security | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wfabricsecurity?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wfabricsecurity) | Zero Trust security system for Hyperledger Fabric. | SHA-256 code integrity, ECDSA P-256 signing, Token Bucket rate-limiting, TTL caching. |
| **`wSnowflake`** | Database ORM | `Development` | Dynamic Snowflake SQL client ORM. | Connection sharing pools, type-safe data loads via Pydantic model serialization. |
| **`wWonka`** | Utility Helpers | `Development` | Internal utilities helper library. | Internal classes, logging setups, reusable core interfaces. |
| **`wauth`** | Security Vault | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wauth?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wauth) | Machine-locked secrets encryption vault. | Fernet encryption using deterministic keys derived from machine-spec ID (OS salted hash). |
| **`wclickhouse`** | Database ORM | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wclickhouse?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wclickhouse) | ClickHouse ORM mapping using clickhouse-connect. | Pydantic v2 schemas, massive bulk inserts, partition tracking helpers. |
| **`wcontainer`** | DevOps Tool | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wcontainer?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wcontainer) | Docker SDK automation utility library. | Automates local container discovery, health status polls, and restarts. |
| **`wdatabricks`** | Database ORM | `Development` | Databricks SQL ORM framework. | Database session pooling, type-safe query parameters mapping. |
| **`wdecorators`** | Code Utility | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wdecorators?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wdecorators) | Reusable high-level decorator collection. | `@retry`, `@timeout`, transaction handlers, execution tracers, periodic loops. |
| **`whaproxy`** | DevOps Tool | `Development` | HAProxy configuration compiler and controller. | Dynamically parses balancing configs and updates active nodes list. |
| **`wimage`** | Code Utility | `Development` | Image resizing and transformation library. | Pillow-based crop, resize, and asset compression utilities. |
| **`wkafka`** | Messaging | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wkafka?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wkafka) | Decorator-based wrapper for Apache Kafka. | `@consumer` decorator mapping to automated topic reading and handling threads. |
| **`wmariadb`** | Database ORM | `Development` | Pydantic ORM wrapper for MariaDB. | Auto-table synchronizer (`TableSync`), CRUD executor, pooled connections. |
| **`wmessenger`** | Messaging | `Development` | Telegram, WhatsApp, and Slack client API. | Simple JSON payload poster, channel listeners, and notification templates. |
| **`wmongo`** | Database ORM | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wmongo?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wmongo) | MongoDB document mapper utilizing Pydantic. | BSON serialization mapping layer, index managers. |
| **`wmysql`** | Database ORM | `Development` | Pydantic ORM wrapper for MySQL. | Connection pooling, dynamic updates serialization mapping. |
| **`wnats`** | Messaging | `Development` | NATS message broker wrappers. | NATS cluster connection pools, pub/sub channel configurations. |
| **`wredis`** | Database ORM | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wredis?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wredis) | Redis sync/async integration & caching suite. | Cache decorators with expiration, token bucket limits, Redis streams handling. |
| **`wsqlite`** | Database ORM | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wsqlite?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wsqlite) | High-performance SQLite ORM. | Connection sharing pools, soft deletion mixins, migration scripts executor. |
| **`wticket`** | Remote API | `Development` | License validator using JSONBin.io backend. | Remote ticket validity validations, usage log uploads. |
| **`wutils`** | Code Utility | `Development` | Common script scheduling and format checkers. | Periodic task wrappers, duration parsing, network checkers. |
| **`wyolo`** | MLOps / Vision | [![PyPI Downloads](https://static.pepy.tech/personalized-badge/wyolo?period=total&units=NONE&left_color=BLACK&right_color=GREEN&left_text=downloads)](https://pepy.tech/projects/wyolo)  | MLflow and S3 YOLO/RT-DETR training workflow. | State machine orchestrator, MLflow metrics logger, autobatching optimization. |
| **`wzeroMQ`** | Messaging | `Development` | IPC/TCP network sockets wrapper using ZeroMQ. | Message formatting, async ZeroMQ socket pooling. |

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
