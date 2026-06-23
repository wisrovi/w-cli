#!/usr/bin/env bash
# docker_test_runner.sh
# Automate running Python tests inside a clean Docker container
# Enforces clean execution environments free of caching or dependencies issues

set -euo pipefail

IMAGE_NAME="wisrovi/w-cli-test-suite:latest"
WORKSPACE_DIR="$(pwd)"

echo "🐳 [1/3] Compiling test execution environment Docker Image..."
# Build temporary container environment mounting pyproject.toml and source directory
docker build -t "${IMAGE_NAME}" -f - "${WORKSPACE_DIR}" <<EOF
FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml setup.py LICENSE README.md requirements.txt ./
# Install local packages including development dependencies in editable mode
RUN pip install --no-cache-dir -e .[dev]
COPY module/ ./module/
COPY test/ ./test/
EOF

echo "🧪 [2/3] Launching PyTest suite inside Docker container..."
docker run --rm \
  -v "${WORKSPACE_DIR}/coverage_reports:/app/coverage_reports" \
  "${IMAGE_NAME}" \
  pytest --cov=module --cov-report=html:/app/coverage_reports/htmlcov --cov-report=term-missing

echo "📊 [3/3] Code Coverage assessment compiled successfully inside /coverage_reports/htmlcov/"
echo "Open standard HTML report at coverage_reports/htmlcov/index.html to view results."
