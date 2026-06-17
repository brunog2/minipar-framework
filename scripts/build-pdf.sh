#!/usr/bin/env bash
# Compila report.tex → report.pdf (via Docker).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

LATEX_IMAGE="${LATEX_IMAGE:-texlive/texlive:latest}"

echo "==> Validando evidências (opcional rápido)..."
if curl -sf http://localhost:3000/health >/dev/null 2>&1; then
  bash "$ROOT/scripts/validate-all.sh" | tail -5
else
  echo "    Gateway offline — pulando validate-all (use docker compose up para E2E)"
fi

echo "==> Compilando report.tex → report.pdf (${LATEX_IMAGE})..."
docker run --rm \
  -v "${ROOT}:/work" \
  -w /work \
  "${LATEX_IMAGE}" \
  bash -lc 'latexmk -pdf -interaction=nonstopmode -f report.tex' || true

if [[ ! -f "${ROOT}/report.pdf" ]]; then
  echo "    ERRO: report.pdf não gerado — veja report.log" >&2
  exit 1
fi
echo "    OK: ${ROOT}/report.pdf ($(du -h report.pdf | cut -f1))"

echo "==> Pacote Overleaf..."
bash "$ROOT/scripts/package-overleaf.sh"

echo ""
echo "Artefatos:"
echo "  - report.pdf          (relatório LaTeX integral)"
echo "  - overleaf-report.zip (upload Overleaf)"
