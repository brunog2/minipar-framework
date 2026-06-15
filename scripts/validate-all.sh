#!/usr/bin/env bash
# Validação completa do plano de conformidade — gera docs/evidence/validation-results.json
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
API="${MINIPAR_API:-http://localhost:3000}"
export ROOT API
EXAMPLES="$ROOT/sources/examples"
EVIDENCE="$ROOT/docs/evidence"
mkdir -p "$EVIDENCE"
RESULTS="$EVIDENCE/validation-results.json"

python3 <<'PY' > "$RESULTS"
import json, os, subprocess, sys, urllib.request, urllib.error
from pathlib import Path

root = Path(os.environ.get("ROOT", "."))
api = os.environ.get("MINIPAR_API", "http://localhost:3000")
examples = root / "sources" / "examples"
results = []

def record(phase, test_id, name, ok, detail=""):
    results.append({
        "phase": phase, "id": test_id, "name": name,
        "status": "PASS" if ok else "FAIL", "detail": str(detail)[:800]
    })

# --- Fase 1-2: minipar-core local ---
sys.path.insert(0, str(root / "packages" / "minipar-core"))
try:
    from minipar_core.pipeline import parse_source
    from minipar_core.translation.interpreter import interpret_ast
    from minipar_core.translation import generate_c

    src15 = (examples / "15_channels.minipar").read_text()
    ast, errs = parse_source(src15)
    r = interpret_ast(ast)
    record("1-2", "E11", "15_channels socket broker", r.exit_code == 0 and "42" in r.output, r.output)

    src09 = (examples / "09_oo_new.minipar").read_text()
    ast, _ = parse_source(src09)
    r = interpret_ast(ast)
    record("2", "E2", "09_oo_new interpretador", r.exit_code == 0 and "woof" in r.output, r.output)

    ast, _ = parse_source(src09)
    rc = generate_c(ast)
    record("5", "E12", "09_oo_new C gcc -O2", rc.exit_code == 0 and "woof" in rc.output, rc.output[:300])

    src11 = (examples / "11_codegen_c.minipar").read_text()
    ast, _ = parse_source(src11)
    rc = generate_c(ast)
    record("5", "E5", "11_codegen_c gcc -O2", rc.exit_code == 0 and "gcc" in rc.output.lower(), rc.output[:200])
except Exception as e:
    record("1-2", "LOCAL", "minipar-core import", False, e)

# --- HTTP tests if gateway up ---
def post(file, target, mode):
    src = (examples / file).read_text()
    body = json.dumps({"sourceCode": src, "targetVariability": target, "executionMode": mode}).encode()
    req = urllib.request.Request(f"{api}/api/v1/process", data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as resp:
        return json.loads(resp.read().decode())

gateway_ok = False
try:
    urllib.request.urlopen(f"{api}/health", timeout=5)
    gateway_ok = True
except Exception:
    pass

record("0", "GW", "gateway health", gateway_ok, api)

if gateway_ok:
    # kind: success = output must contain needle; failure = success false + needle in error/output
    cases = [
        ("1", "E1", "08_interpreter_ok.minipar", "INTERPRETER", "LOCAL", "success", "ok"),
        ("1", "E7", "05_parse_extends_missing.minipar", "INTERPRETER", "LOCAL", "failure", "parser"),
        ("2", "E6", "12_codegen_rust_stub.minipar", "RUST", "LOCAL", "success", "rustc"),
        ("3", "E3", "13_sierpinski.minipar", "INTERPRETER", "LOCAL", "success", "*"),
        ("3", "E4", "08_interpreter_ok.minipar", "INTERPRETER", "DISTRIBUTED_SOCKETS", "success", "PC"),
        ("3", "E10", "14_distributed_menu.minipar", "INTERPRETER", "DISTRIBUTED_SOCKETS", "success", "900"),
        ("4", "E8", "04_semantic_extends_unknown.minipar", "INTERPRETER", "LOCAL", "failure", "semantic"),
        ("6", "E9", "16_codegen_python.minipar", "PYTHON", "LOCAL", "success", "Python"),
    ]
    for phase, tid, fname, target, mode, kind, needle in cases:
        try:
            data = post(fname, target, mode)
            out = (data.get("output") or "") + (data.get("error") or "")
            if kind == "success":
                ok = bool(data.get("success")) and needle.lower() in out.lower()
            else:
                ok = data.get("success") is False and needle.lower() in out.lower()
            record(phase, tid, fname, ok, out[:400])
        except Exception as e:
            record(phase, tid, fname, False, e)

    for path, name in [
        ("/api/v1/variants", "GET variants"),
        ("/api/v1/recommendations", "GET recommendations"),
        ("/api/v1/services/health", "GET services health"),
    ]:
        try:
            with urllib.request.urlopen(f"{api}{path}", timeout=15) as resp:
                data = json.loads(resp.read().decode())
            if path.endswith("services/health"):
                ok = (
                    isinstance(data, list)
                    and len(data) >= 9
                    and all(item.get("status") == "ok" for item in data)
                )
                record("6", name, name, ok, str(data)[:200])
            else:
                record("6", name, name, bool(data), str(data)[:200])
        except Exception as e:
            record("6", name, name, False, e)

print(json.dumps({"api": api, "gateway": gateway_ok, "tests": results}, indent=2, ensure_ascii=False))
PY

echo "Resultados em $RESULTS"
python3 -c "
import json
d=json.load(open('$RESULTS'))
passed=sum(1 for t in d['tests'] if t['status']=='PASS')
total=len(d['tests'])
print(f'PASS {passed}/{total}')
for t in d['tests']:
    print(f\"  [{t['status']}] {t['id']}: {t['name']}\")
"
