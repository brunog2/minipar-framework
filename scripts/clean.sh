#!/usr/bin/env bash
# Remove artefatos gerados localmente (LaTeX, builds, caches). Não apaga código-fonte.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "==> LaTeX (report.* auxiliares e PDFs gerados)"
rm -f report.aux report.log report.fls report.fdb_latexmk report.synctex.gz \
      report.toc report.out report.bbl report.blg report.nav report.snm report.vrb \
      report.pdf report-md.pdf overleaf-report.zip

echo "==> Python caches"
find . -type d -name '__pycache__' -not -path './node_modules/*' -prune -exec rm -rf {} + 2>/dev/null || true
find . -type d \( -name '.pytest_cache' -o -name '.mypy_cache' -o -name '.ruff_cache' -o -name 'htmlcov' -o -name '*.egg-info' \) \
  -not -path './node_modules/*' -prune -exec rm -rf {} + 2>/dev/null || true

echo "==> Node / Angular builds"
rm -rf api-gateway/dist frontend/dist frontend/.angular
find . -name '*.tsbuildinfo' -not -path '*/node_modules/*' -delete 2>/dev/null || true

echo "==> OS / editor"
find . -name '.DS_Store' -not -path './node_modules/*' -delete 2>/dev/null || true
find . -name '*~' -not -path './node_modules/*' -delete 2>/dev/null || true
find . \( -name '*.swp' -o -name '*.swo' \) -not -path './node_modules/*' -delete 2>/dev/null || true

echo "Limpeza concluída em ${ROOT}"
