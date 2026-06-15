#!/usr/bin/env bash
# Smoke E2E — valida fixtures principais (requer docker compose ou gateway :3000)
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API="${MINIPAR_API:-http://localhost:3000}"
EXAMPLES="$ROOT/sources/examples"

post() {
  local file="$1" target="$2" mode="$3" label="$4"
  echo "==> $label"
  python3 - "$API" "$file" "$target" "$mode" <<'PY'
import json, sys, urllib.request
api, path, target, mode = sys.argv[1:5]
src = open(path, encoding="utf-8").read()
body = json.dumps({"sourceCode": src, "targetVariability": target, "executionMode": mode}).encode()
req = urllib.request.Request(f"{api}/api/v1/process", data=body, headers={"Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=120) as resp:
    data = json.loads(resp.read().decode())
print("success:", data.get("success"))
print((data.get("output") or data.get("error") or "")[:500])
PY
  echo ""
}

cd "$ROOT/packages/minipar-core"
python3 -c "
from minipar_core.pipeline import parse_source
from minipar_core.translation.interpreter import interpret_ast
for name in ['15_channels.minipar']:
    ast, _ = parse_source(open('$EXAMPLES/'+name).read())
    r = interpret_ast(ast)
    assert r.exit_code == 0, r.output
    print('OK local', name, r.output.strip())
"

if curl -sf "$API/health" >/dev/null 2>&1; then
  post "$EXAMPLES/08_interpreter_ok.minipar" INTERPRETER LOCAL "E1 interpretador"
  post "$EXAMPLES/09_oo_new.minipar" INTERPRETER LOCAL "E2 OO"
  post "$EXAMPLES/13_sierpinski.minipar" INTERPRETER LOCAL "E3 fractal"
  post "$EXAMPLES/11_codegen_c.minipar" C LOCAL "E5 C gcc"
  post "$EXAMPLES/16_codegen_python.minipar" PYTHON LOCAL "E9 Python"
  post "$EXAMPLES/08_interpreter_ok.minipar" INTERPRETER DISTRIBUTED_SOCKETS "E4 3 máquinas"
  post "$EXAMPLES/14_distributed_menu.minipar" INTERPRETER DISTRIBUTED_SOCKETS "E10 menu MiniPar"
  echo "E2E smoke HTTP concluído."
else
  echo "Gateway indisponível em $API — apenas testes locais minipar-core executados."
fi
