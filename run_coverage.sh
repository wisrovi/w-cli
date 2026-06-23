#!/usr/bin/env bash
# run_coverage.sh
# Calculates unit test coverage locally for rapid development iteration cycles

set -euo pipefail

echo "🧪 Running pytest local coverage calculation..."
PYTHONPATH=. pytest --cov=module --cov-report=html:coverage_reports/htmlcov --cov-report=term-missing

echo "✓ Local coverage report calculated in coverage_reports/htmlcov/index.html"

