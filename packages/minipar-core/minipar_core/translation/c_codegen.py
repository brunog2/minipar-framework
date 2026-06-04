"""Gerador C a partir de TAC — MVP Fase 2 (reuso projeto_compiladores)."""

from __future__ import annotations

from typing import Dict, List, Optional, Set

from minipar_core.translation.tac import TAC


class SimpleCCodeGenerator:
    """Gera C compilável para subset MVP: print, funções, main entry."""

    def __init__(self) -> None:
        self.functions: Dict[str, tuple] = {}  # name -> (body, params)
        self.current_fn: Optional[str] = None
        self.fn_body: List[str] = []
        self.main_body: List[str] = []
        self.strings: Dict[str, str] = {}
        self.string_id = 0
        self.pending_params: List[str] = []
        self.oo_types: Dict[str, str] = {}
        self.oo_classes: set = set()
        self.pending_method: tuple | None = None
        self.instance_methods: Set[str] = set()
        # Passagem 1: coleta de campos reais por classe (SET_PROP / GET_PROP)
        self.class_fields: Dict[str, list] = {}
        # Bug A2: function declaration params (FUNC_PARAM) vs call args (PARAM)
        self._func_params: List[str] = []
        # Bug A4: funções que retornam valor
        self._fn_returns_value: Set[str] = set()
        # Bug A5: classe atual do método sendo gerado
        self._current_method_cls: Optional[str] = None
        # Track declared variables per function to avoid redeclaration
        self._declared_vars: Set[str] = set()

    def _esc(self, s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    def _str_label(self, raw: str) -> str:
        if raw not in self.strings:
            self.strings[raw] = f"str_{self.string_id}"
            self.string_id += 1
        return self.strings[raw]

    def _target_body(self) -> List[str]:
        if self.current_fn:
            return self.fn_body
        return self.main_body

    def _emit(self, line: str) -> None:
        self._target_body().append(line)

    def _resolve_var(self, name: str) -> str:
        """Se 'name' for campo da classe atual, retorna 'this->name'."""
        if (self._current_method_cls and
                name in self.class_fields.get(self._current_method_cls, [])):
            return f"this->{name}"
        return name

    def generate(self, instructions: List[TAC]) -> str:
        self.functions = {}
        self.current_fn = None
        self.fn_body = []
        self.main_body = []
        self.pending_params = []
        self.strings = {}
        self.string_id = 0
        self.oo_types = {}
        self.oo_classes = set()
        self.class_fields = {}
        self.pending_method = None
        self.instance_methods = set()
        self._func_params = []
        self._fn_returns_value = set()
        self._current_method_cls = None
        self._declared_vars = set()

        # Passagem 1: coletar campos de classe via SET_PROP e GET_PROP
        for instr in instructions:
            if instr.op == "SET_PROP":
                pass
            if instr.op == "NEW":
                cls = str(instr.arg1)
                self.oo_classes.add(cls)

        # Passagem 1b: rastrear oo_types e coletar campos em ordem
        _types_tmp: Dict[str, str] = {}
        _fields_order: Dict[str, list] = {}
        for instr in instructions:
            if instr.op == "NEW":
                cls = str(instr.arg1)
                result = str(instr.result)
                _types_tmp[result] = cls
                if cls not in _fields_order:
                    _fields_order[cls] = []
            if instr.op == "ASSIGN":
                src = str(instr.arg1)
                dst = str(instr.result)
                if src in _types_tmp:
                    _types_tmp[dst] = _types_tmp[src]
            if instr.op in ("SET_PROP", "GET_PROP"):
                receiver = str(instr.arg1)
                prop = str(instr.arg2)
                cls = _types_tmp.get(receiver)
                if cls:
                    if cls not in _fields_order:
                        _fields_order[cls] = []
                    if prop not in _fields_order[cls]:
                        _fields_order[cls].append(prop)
                # Also collect fields accessed via 'this' by tracking the current method class
            if instr.op == "FUNC_BEGIN":
                fn = str(instr.arg1)
                if fn and "_" in fn:
                    cls, method = fn.split("_", 1)
                    if cls not in ("Global",):
                        if cls not in _fields_order:
                            _fields_order[cls] = []
                        self.oo_classes.add(cls)

        # Also collect fields from SET_PROP/GET_PROP on 'this' within methods
        _current_fn_cls = None
        for instr in instructions:
            if instr.op == "FUNC_BEGIN":
                fn = str(instr.arg1)
                if fn and "_" in fn:
                    cls_part = fn.split("_", 1)[0]
                    _current_fn_cls = cls_part if cls_part not in ("Global", "Main") else None
                else:
                    _current_fn_cls = None
            elif instr.op in ("SET_PROP", "GET_PROP") and str(instr.arg1) == "this":
                if _current_fn_cls:
                    prop = str(instr.arg2)
                    if _current_fn_cls not in _fields_order:
                        _fields_order[_current_fn_cls] = []
                    if prop not in _fields_order[_current_fn_cls]:
                        _fields_order[_current_fn_cls].append(prop)

        self.class_fields = _fields_order

        # Passagem 2: emissão
        for instr in instructions:
            self._emit_instr(instr)

        if self.current_fn:
            self.functions[self.current_fn] = (self.fn_body, self._func_params)
            self.current_fn = None
            self.fn_body = []

        out: List[str] = [
            "/* Generated by MiniPar ms-codegen-c (Fase 2+) */",
            "#include <stdio.h>",
            "#include <stdlib.h>",
            "#include <string.h>",
            "#include <math.h>",
            "",
        ]

        # Geração de structs com campos reais
        if self.class_fields:
            # Forward declarations
            for cls in self.class_fields:
                out.append(f"typedef struct {cls} {cls};")
            out.append("")
            for cls, fields in self.class_fields.items():
                out.append(f"struct {cls} {{")
                if fields:
                    for field_name in fields:
                        out.append(f"    double {field_name};")
                else:
                    out.append("    int _tag;")
                out.append("};")
                # Constructor
                out.append(f"{cls}* {cls}_new(void) {{")
                out.append(f"    {cls}* self = ({cls}*)calloc(1, sizeof({cls}));")
                out.append("    return self;")
                out.append("}")
                out.append("")
        elif self.oo_classes:
            for cls in sorted(self.oo_classes):
                out.append(f"typedef struct {{ int _tag; }} {cls};")
                out.append(f"void* {cls}_new(void) {{ return calloc(1, sizeof({cls})); }}")
                out.append("")

        if self.strings:
            out.append("/* string literals */")
            for raw, label in self.strings.items():
                inner = raw[1:-1] if raw.startswith('"') else raw
                out.append(f'const char* {label} = "{self._esc(inner)}";')
            out.append("")

        # Forward-declare all functions before their definitions
        for name, (body, params) in self.functions.items():
            return_type = "double" if name in self._fn_returns_value else "void"
            if name in self.instance_methods:
                cls = name.split("_", 1)[0] if "_" in name else None
                if cls and self.class_fields.get(cls) is not None:
                    param_str = f"{cls}* this"
                else:
                    param_str = "void* this"
                if params:
                    param_str += ", " + ", ".join(f"double {p}" for p in params)
            else:
                param_str = ", ".join(f"double {p}" for p in params) or "void"
            out.append(f"{return_type} {name}({param_str});")
        if self.functions:
            out.append("")

        for name, (body, params) in self.functions.items():
            return_type = "double" if name in self._fn_returns_value else "void"
            if name in self.instance_methods:
                cls = name.split("_", 1)[0] if "_" in name else None
                if cls and self.class_fields.get(cls) is not None:
                    param_str = f"{cls}* this"
                else:
                    param_str = "void* this"
                if params:
                    param_str += ", " + ", ".join(f"double {p}" for p in params)
            else:
                param_str = ", ".join(f"double {p}" for p in params) or "void"
            out.append(f"{return_type} {name}({param_str}) {{")
            out.extend(f"    {line}" for line in body)
            out.append("}")
            out.append("")

        out.append("int main(void) {")
        if "Main_run" in self.functions:
            # Main_run is an instance method if Main is in class_fields
            if self.class_fields.get("Main") is not None:
                out.append("    Main* _main = Main_new();")
                out.append("    Main_run(_main);")
            else:
                out.append("    Main_run();")
        elif self.main_body:
            out.extend(f"    {line}" for line in self.main_body)
        out.append("    return 0;")
        out.append("}")
        return "\n".join(out)

    def _emit_instr(self, instr: TAC) -> None:
        op = instr.op

        if op == "FUNC_BEGIN":
            if self.current_fn:
                self.functions[self.current_fn] = (self.fn_body, self._func_params)
            self.current_fn = instr.arg1
            self.fn_body = []
            self._func_params = []
            self._declared_vars = set()
            if isinstance(self.current_fn, str) and "_" in self.current_fn:
                cls, method = self.current_fn.split("_", 1)
                if cls not in ("Global",):
                    # All class methods (including Main.fib) are instance methods
                    # except plain entry-point functions
                    self.instance_methods.add(self.current_fn)
                    self.oo_classes.add(cls)
                # A5: track current method's class for this-> resolution
                self._current_method_cls = cls if cls not in ("Global",) else None
            else:
                self._current_method_cls = None
            return

        if op == "FUNC_END":
            if self.current_fn:
                self.functions[self.current_fn] = (self.fn_body, self._func_params)
            self.current_fn = None
            self.fn_body = []
            self._current_method_cls = None
            self._declared_vars = set()
            return

        if op in ("CALL_MAIN",):
            return

        # A2: FUNC_PARAM = function declaration parameter, PARAM = call argument
        if op == "FUNC_PARAM":
            self._func_params.append(str(instr.arg1))
            return

        if op == "PARAM":
            self.pending_params.append(str(instr.arg1))
            return

        if op == "PRINT":
            val = instr.arg1
            newline = instr.arg2 == "1"
            if isinstance(val, str) and val.startswith('"'):
                label = self._str_label(val)
                if newline:
                    self._emit(f'printf("%s\\n", {label});')
                else:
                    self._emit(f'printf("%s", {label});')
            else:
                resolved = self._resolve_var(str(val))
                if newline:
                    self._emit(f'printf("%g\\n", (double)({resolved}));')
                else:
                    self._emit(f'printf("%g", (double)({resolved}));')
            return

        if op == "ASSIGN":
            src = str(instr.arg1)
            dst = str(instr.result)
            if src in self.oo_types:
                cls = self.oo_types[src]
                self.oo_types[dst] = cls
                if dst not in self._declared_vars:
                    self._declared_vars.add(dst)
                    if self.class_fields.get(cls) is not None:
                        self._emit(f"{cls}* {dst} = ({cls}*)({src});")
                    else:
                        self._emit(f"void* {dst} = (void*)({src});")
                else:
                    self._emit(f"{dst} = ({cls}*)({src});")
            else:
                resolved_src = self._resolve_var(src)
                if dst not in self._declared_vars:
                    self._declared_vars.add(dst)
                    self._emit(f"double {dst} = (double)({resolved_src});")
                else:
                    self._emit(f"{dst} = (double)({resolved_src});")
            return

        if op == "RETURN":
            if instr.arg1 is not None:
                self._fn_returns_value.add(self.current_fn)
                val = self._resolve_var(str(instr.arg1))
                self._emit(f"return (double)({val});")
            else:
                self._emit("return;")
            return

        # A1: extended operator set — both mnemonic and symbol forms
        ARITH_OPS = {"+", "-", "*", "/"}
        CMP_OPS = {"<", ">", "==", "!=", "<=", ">=", "LT", "GT", "EQ", "NE", "LE", "GE"}
        C_OP_MAP = {
            "+": "+", "-": "-", "*": "*", "/": "/",
            "LT": "<", "GT": ">", "EQ": "==", "NE": "!=", "LE": "<=", "GE": ">=",
            "<": "<", ">": ">", "==": "==", "!=": "!=", "<=": "<=", ">=": ">=",
        }

        if op == "%":
            a, b, r = self._resolve_var(str(instr.arg1)), self._resolve_var(str(instr.arg2)), instr.result
            self._emit(f"double {r} = fmod((double)({a}), (double)({b}));")
            return

        if op in ARITH_OPS | CMP_OPS:
            a = self._resolve_var(str(instr.arg1))
            b = self._resolve_var(str(instr.arg2))
            r = instr.result
            c_op = C_OP_MAP[op]
            if op in CMP_OPS:
                self._emit(f"double {r} = ((double)({a}) {c_op} (double)({b})) ? 1.0 : 0.0;")
            else:
                self._emit(f"double {r} = (double)({a}) {c_op} (double)({b});")
            return

        if op == "UNARY":
            # TAC UNARY: arg1=operator, arg2=operand, result=result
            unary_op = str(instr.arg1)
            operand = self._resolve_var(str(instr.arg2))
            self._emit(f"double {instr.result} = ({unary_op}(double)({operand}));")
            return

        if op == "LABEL":
            # Semicolon after label allows declarations to follow (C11/C17 compliant)
            self._emit(f"{instr.arg1}: ;")
            return

        if op == "GOTO":
            self._emit(f"goto {instr.arg1};")
            return

        if op == "IF_FALSE":
            cond = self._resolve_var(str(instr.arg1))
            self._emit(f"if (!((double)({cond}))) goto {instr.result};")
            return

        if op == "CALL":
            n_args = int(instr.arg2 or 0)
            args = ", ".join(self.pending_params[-n_args:]) if n_args else ""
            self.pending_params = self.pending_params[:-n_args] if n_args else self.pending_params
            name = str(instr.arg1)
            result = instr.result
            if name in self._fn_returns_value:
                self._emit(f"double {result} = {name}({args});")
            else:
                self._emit(f"{name}({args});")
            return

        if op in (
            "SEQ_BEGIN",
            "SEQ_END",
            "PAR_BEGIN",
            "PAR_END",
            "THREAD_START",
            "THREAD_END",
        ):
            return

        if op == "LIST_LEN":
            self._emit(f"double {instr.result} = 0; /* list MVP */")
            return

        if op == "LIST_GET":
            self._emit(f"double {instr.result} = 0; /* list get MVP */")
            return

        if op in ("METHOD_CALL", "NEW", "GET_PROP", "SET_PROP", "METHOD_ARGS"):
            if op == "NEW":
                cls = str(instr.arg1)
                n_args = int(instr.arg2 or 0)
                result = instr.result
                self.oo_classes.add(cls)
                self.oo_types[str(result)] = cls
                if n_args:
                    self.pending_params = self.pending_params[:-n_args]
                fields = self.class_fields.get(cls)
                if fields is not None:
                    self._emit(f"{cls}* {result} = {cls}_new();")
                else:
                    self._emit(f"void* {result} = (void*){cls}_new();")
                return

            if op == "METHOD_CALL":
                self.pending_method = (
                    str(instr.arg1),
                    str(instr.arg2),
                    str(instr.result),
                )
                return

            if op == "METHOD_ARGS":
                if not self.pending_method:
                    return
                receiver, method, result = self.pending_method
                self.pending_method = None
                n_args = int(instr.arg1 or 0)
                extra = self.pending_params[-n_args:] if n_args else []
                self.pending_params = self.pending_params[:-n_args] if n_args else self.pending_params
                cls = self.oo_types.get(receiver, self._current_method_cls or "Object")
                fn = f"{cls}_{method}"
                call_args = [receiver] + extra
                # A3/A4: declare result and capture return value if function returns
                if fn in self._fn_returns_value:
                    self._emit(f"double {result} = {fn}({', '.join(call_args)});")
                else:
                    # Emit placeholder declaration; actual return tracking happens lazily
                    # We need to forward-check: emit a call that captures result
                    # For now, emit the call and assign result (works for void functions too
                    # as a no-op if result is discarded)
                    self._emit(f"double {result} = 0;  /* result of {fn} */")
                    self._emit(f"{fn}({', '.join(call_args)});")
                return

            if op == "GET_PROP":
                receiver = str(instr.arg1)
                prop = str(instr.arg2)
                result = instr.result
                # If receiver is 'this', use direct struct member access
                if receiver == "this":
                    self._emit(f"double {result} = this->{prop};")
                else:
                    cls = self.oo_types.get(receiver, "void")
                    if cls != "void" and self.class_fields.get(cls) is not None:
                        self._emit(f"double {result} = (({cls}*){receiver})->{prop};")
                    else:
                        self._emit(f"double {result} = 0; /* GET_PROP {receiver}.{prop} */")
                return

            if op == "SET_PROP":
                receiver = str(instr.arg1)
                prop = str(instr.arg2)
                value = self._resolve_var(str(instr.result))
                # If receiver is 'this', use direct struct member access
                if receiver == "this":
                    self._emit(f"this->{prop} = (double)({value});")
                else:
                    cls = self.oo_types.get(receiver, "void")
                    if cls != "void" and self.class_fields.get(cls) is not None:
                        self._emit(f"(({cls}*){receiver})->{prop} = (double)({value});")
                    else:
                        self._emit(f"/* SET_PROP {receiver}.{prop} = {value} */")
                return

        self._emit(f"/* unhandled TAC: {instr} */")
