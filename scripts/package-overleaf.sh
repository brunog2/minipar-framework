#!/usr/bin/env bash
# Gera ZIP pronto para upload no Overleaf (report.tex + figuras).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="${ROOT}/overleaf-report.zip"
TMP="$(mktemp -d)"

mkdir -p "${TMP}/docs/figures/ui"
cp "${ROOT}/report.tex" "${TMP}/"
cp "${ROOT}/docs/report-embedded-contracts.tex" "${TMP}/docs/"
cp "${ROOT}/docs/report-embedded-appendices.tex" "${TMP}/docs/"
cp "${ROOT}/docs/report-embedded-api.tex" "${TMP}/docs/"
cp "${ROOT}/docs/report-embedded-pseudocode.tex" "${TMP}/docs/"
cp "${ROOT}/docs/figures/"*.png "${TMP}/docs/figures/" 2>/dev/null || true
cp "${ROOT}/docs/figures/ui/"*.png "${TMP}/docs/figures/ui/" 2>/dev/null || true
if [[ -f "${ROOT}/logo_ufal.png" ]]; then
  cp "${ROOT}/logo_ufal.png" "${TMP}/"
fi

(cd "${TMP}" && zip -rq "${OUT}" .)
rm -rf "${TMP}"
echo "Pacote Overleaf: ${OUT}"
echo "No Overleaf: New Project → Upload Project → selecione overleaf-report.zip"
echo "Compilador: pdfLaTeX (menu esquerdo → Recompile)"
