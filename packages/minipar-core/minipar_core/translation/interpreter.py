"""Interpretador MiniPar — execução direta da AST (port cl-minipar MVP)."""

from __future__ import annotations

import io
import json
import multiprocessing
import pickle
import socket as _socket
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

from minipar_core import ast_nodes as n
from minipar_core.translation.ast_from_json import from_dict
from minipar_core.translation.base_translator import (
    AbstractBackendTranslator,
    TranslationResult,
)


class ReturnSignal(Exception):
    def __init__(self, value: Any = None):
        self.value = value


class BreakSignal(Exception):
    pass


class ContinueSignal(Exception):
    pass


@dataclass
class MiniFunction:
    name: str
    parameters: List[n.Parameter]
    body: n.Block
    closure: "Environment"


@dataclass
class MiniClass:
    name: str
    super_class: Optional["MiniClass"]
    fields: Dict[str, Any] = field(default_factory=dict)
    methods: Dict[str, n.MethodDecl] = field(default_factory=dict)


@dataclass
class MiniInstance:
    klass: MiniClass
    fields: Dict[str, Any] = field(default_factory=dict)


class Environment:
    def __init__(self, parent: Optional["Environment"] = None):
        self.parent = parent
        self.values: Dict[str, Any] = {}

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeError(f"Undefined variable: {name}")

    def assign(self, name: str, value: Any) -> None:
        if name in self.values:
            self.values[name] = value
            return
        if self.parent:
            self.parent.assign(name, value)
            return
        raise RuntimeError(f"Undefined variable: {name}")


class Interpreter:
    def __init__(self, output: io.StringIO | None = None):
        self.globals = Environment()
        self.env = self.globals
        self.output = output or io.StringIO()
        self.this_instance: MiniInstance | None = None
        self.classes: Dict[str, MiniClass] = {}
        self._print_hook: Optional[Callable[[str], None]] = None
        # multiprocessing.Queue so channels work across both threads and forked processes
        self._channels: Dict[str, Any] = {}

    def _output(self, text: str) -> None:
        if self._print_hook:
            self._print_hook(text)
        else:
            self.output.write(text)

    def execute(self, program: n.Program) -> str:
        for decl in program.declarations:
            self.exec(decl)
        self._invoke_main_entry()
        return self.output.getvalue()

    def _invoke_main_entry(self) -> None:
        main_class = self.classes.get("Main")
        if not main_class or "run" not in main_class.methods:
            return
        instance = MiniInstance(main_class, dict(main_class.fields))
        self._call_method(instance, main_class.methods["run"], [])

    def exec(self, node) -> Any:
        if node is None:
            return None
        if isinstance(node, n.Program):
            return self.execute(node)
        if isinstance(node, n.ClassDecl):
            return self.exec_class(node)
        if isinstance(node, n.MethodDecl):
            return None
        if isinstance(node, n.VarDecl):
            return self.exec_var_decl(node)
        if isinstance(node, n.FuncDecl):
            return self.exec_func_decl(node)
        if isinstance(node, n.Block):
            return self.exec_block(node)
        if isinstance(node, n.SeqBlock):
            return self.exec_seq(node.statements)
        if isinstance(node, n.ParBlock):
            return self.exec_par(node.statements)
        if isinstance(node, n.IfStmt):
            return self.exec_if(node)
        if isinstance(node, n.WhileStmt):
            return self.exec_while(node)
        if isinstance(node, n.ForStmt):
            return self.exec_for(node)
        if isinstance(node, n.PrintStmt):
            return self.exec_print(node)
        if isinstance(node, n.ReturnStmt):
            raise ReturnSignal(self.eval(node.value) if node.value else None)
        if isinstance(node, n.BreakStmt):
            raise BreakSignal()
        if isinstance(node, n.ContinueStmt):
            raise ContinueSignal()
        if isinstance(node, n.ExprStmt):
            if isinstance(node.expression, n.Assignment):
                return self.exec_assignment(node.expression)
            if isinstance(node.expression, n.PropertyAssign):
                return self.exec_property_assign(node.expression)
            return self.eval(node.expression)
        if isinstance(node, n.Assignment):
            return self.exec_assignment(node)
        if isinstance(node, n.PropertyAssign):
            return self.exec_property_assign(node)
        if isinstance(node, n.SuperCall):
            return self.exec_super_call(node)
        if isinstance(node, n.ChannelDecl):
            return self.exec_channel_decl(node)
        if isinstance(node, n.SendStmt):
            return self.exec_send(node)
        if isinstance(node, n.ReceiveStmt):
            return self.exec_receive(node)
        return self.eval(node)

    def exec_class(self, node: n.ClassDecl) -> None:
        super_class = self.classes.get(node.extends) if node.extends else None
        fields: Dict[str, Any] = {}
        methods: Dict[str, n.MethodDecl] = {}
        if super_class:
            fields.update(super_class.fields)
            methods.update(super_class.methods)
        for member in node.members:
            if isinstance(member, n.VarDecl):
                fields[member.name] = (
                    self.eval(member.initializer) if member.initializer else None
                )
            elif isinstance(member, n.MethodDecl):
                methods[member.name] = member
        klass = MiniClass(node.name, super_class, fields, methods)
        self.classes[node.name] = klass
        self.globals.define(node.name, klass)

    def exec_var_decl(self, node: n.VarDecl) -> None:
        value = self.eval(node.initializer) if node.initializer else None
        self.env.define(node.name, value)

    def exec_func_decl(self, node: n.FuncDecl) -> None:
        fn = MiniFunction(node.name, node.parameters, node.body, self.env)
        self.globals.define(node.name, fn)

    def exec_block(self, node: n.Block) -> None:
        for stmt in node.statements:
            self.exec(stmt)

    def exec_seq(self, statements: List) -> None:
        for stmt in statements:
            self.exec(stmt)

    def exec_par(self, statements: List) -> None:
        if not statements:
            return

        # Snapshot: only JSON-serializable primitives from current env chain
        env_snapshot: Dict[str, Any] = {}
        env = self.env
        while env is not None:
            for k, v in env.values.items():
                if k not in env_snapshot and isinstance(v, (str, int, float, bool, type(None))):
                    env_snapshot[k] = v
            env = env.parent

        shared_data = pickle.dumps({"classes": self.classes, "env": env_snapshot})
        stmt_datas = [pickle.dumps(s) for s in statements]

        server = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        server.setsockopt(_socket.SOL_SOCKET, _socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        port = server.getsockname()[1]
        server.listen(len(statements))
        server.settimeout(30)

        procs = [
            multiprocessing.Process(
                target=_par_worker,
                args=(sd, shared_data, port, self._channels),
                daemon=True,
            )
            for sd in stmt_datas
        ]
        for p in procs:
            p.start()

        results = []
        for _ in statements:
            try:
                conn, _ = server.accept()
                data = b""
                while not data.endswith(b"\n"):
                    chunk = conn.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                conn.close()
                results.append(json.loads(data.decode()))
            except Exception:
                results.append({"output": [], "env": {}})

        for p in procs:
            p.join(timeout=30)
        server.close()

        for r in results:
            for line in r.get("output", []):
                self._output(line)
        # Propagate env updates (e.g. receive(ch, result)) back to parent env
        for r in results:
            for k, v in r.get("env", {}).items():
                try:
                    self.env.assign(k, v)
                except RuntimeError:
                    self.env.define(k, v)

    def exec_channel_decl(self, node: n.ChannelDecl) -> None:
        self._channels[node.name] = multiprocessing.Queue()

    def exec_send(self, node: n.SendStmt) -> None:
        value = self.eval(node.value)
        ch = self._channels.get(node.channel)
        if ch is None:
            raise RuntimeError(f"Channel not declared: {node.channel}")
        ch.put(value)

    def exec_receive(self, node: n.ReceiveStmt) -> None:
        ch = self._channels.get(node.channel)
        if ch is None:
            raise RuntimeError(f"Channel not declared: {node.channel}")
        value = ch.get()
        try:
            self.env.assign(node.target, value)
        except RuntimeError:
            self.env.define(node.target, value)

    def exec_if(self, node: n.IfStmt) -> None:
        if self._truthy(self.eval(node.condition)):
            self.exec(node.then_branch)
        elif node.else_branch:
            self.exec(node.else_branch)

    def exec_while(self, node: n.WhileStmt) -> None:
        while self._truthy(self.eval(node.condition)):
            try:
                self.exec(node.body)
            except ContinueSignal:
                continue
            except BreakSignal:
                break

    def exec_for(self, node: n.ForStmt) -> None:
        iterable = self.eval(node.iterable)
        if not isinstance(iterable, list):
            raise RuntimeError("For loop requires a list iterable")
        for item in iterable:
            self.env.define(node.variable.name, item)
            try:
                self.exec(node.body)
            except ContinueSignal:
                continue
            except BreakSignal:
                break

    def exec_print(self, node: n.PrintStmt) -> None:
        parts = [self._format_value(self.eval(arg)) for arg in node.arguments]
        text = " ".join(parts)
        if node.newline:
            self._output(text + "\n")
        else:
            self._output(text)

    def exec_assignment(self, node: n.Assignment) -> Any:
        value = self.eval(node.value)
        self.env.assign(node.name, value)
        return value

    def exec_super_call(self, node: n.SuperCall) -> None:
        if self.this_instance is None:
            raise RuntimeError("'super()' outside instance method")
        super_class = self.this_instance.klass.super_class
        if not super_class:
            raise RuntimeError("Class has no superclass")
        args = [self.eval(a) for a in node.arguments]
        ctor = super_class.methods.get("constructor") or super_class.methods.get(
            super_class.name
        )
        if ctor:
            self._call_method(self.this_instance, ctor, args)

    def exec_property_assign(self, node: n.PropertyAssign) -> None:
        receiver = self.eval(node.receiver)
        value = self.eval(node.value)
        if isinstance(receiver, MiniInstance):
            receiver.fields[node.property_name] = value
        else:
            raise RuntimeError("Property assign requires object instance")

    def eval(self, node) -> Any:
        if node is None:
            return None
        if isinstance(node, n.NumberLiteral):
            return node.value
        if isinstance(node, n.StringLiteral):
            return node.value
        if isinstance(node, n.BoolLiteral):
            return node.value
        if isinstance(node, n.Variable):
            return self.env.get(node.name)
        if isinstance(node, n.ThisExpr):
            if self.this_instance is None:
                raise RuntimeError("'this' outside instance method")
            return self.this_instance
        if isinstance(node, n.BinaryOp):
            return self.eval_binary(node)
        if isinstance(node, n.UnaryOp):
            return self.eval_unary(node)
        if isinstance(node, n.FuncCall):
            return self.eval_func_call(node)
        if isinstance(node, n.MethodCall):
            return self.eval_method_call(node)
        if isinstance(node, n.NewInstance):
            return self.eval_new_instance(node)
        if isinstance(node, n.PropertyAccess):
            return self.eval_property_access(node)
        if isinstance(node, n.ListLiteral):
            return [self.eval(e) for e in node.elements]
        if isinstance(node, n.DictLiteral):
            return {self.eval(k): self.eval(v) for k, v in node.pairs}
        if isinstance(node, n.IndexAccess):
            obj = self.eval(node.object)
            idx = self.eval(node.index)
            return obj[int(idx)]
        raise RuntimeError(f"Cannot evaluate node: {node.__class__.__name__}")

    def eval_binary(self, node: n.BinaryOp) -> Any:
        left = self.eval(node.left)
        right = self.eval(node.right)
        op = node.operator
        if op == "+":
            if isinstance(left, str) or isinstance(right, str):
                return self._format_value(left) + self._format_value(right)
            return left + right
        if op == "-":
            return left - right
        if op == "*":
            return left * right
        if op == "/":
            return left / right
        if op == "%":
            return left % right
        if op == "==":
            return left == right
        if op == "!=":
            return left != right
        if op == "<":
            return left < right
        if op == ">":
            return left > right
        if op == "<=":
            return left <= right
        if op == ">=":
            return left >= right
        if op == "&&":
            return self._truthy(left) and self._truthy(right)
        if op == "||":
            return self._truthy(left) or self._truthy(right)
        raise RuntimeError(f"Unknown operator: {op}")

    def eval_unary(self, node: n.UnaryOp) -> Any:
        val = self.eval(node.operand)
        if node.operator == "-":
            return -val
        if node.operator == "!":
            return not self._truthy(val)
        raise RuntimeError(f"Unknown unary: {node.operator}")

    def eval_func_call(self, node: n.FuncCall) -> Any:
        callee = self.env.get(node.name)
        args = [self.eval(a) for a in node.arguments]
        if isinstance(callee, MiniFunction):
            return self._call_function(callee, args)
        raise RuntimeError(f"Not callable: {node.name}")

    def eval_method_call(self, node: n.MethodCall) -> Any:
        receiver = self.eval(node.receiver)
        args = [self.eval(a) for a in node.arguments]
        if isinstance(receiver, MiniInstance):
            method = receiver.klass.methods.get(node.method)
            if not method:
                raise RuntimeError(
                    f"Method '{node.method}' not found on {receiver.klass.name}"
                )
            return self._call_method(receiver, method, args)
        raise RuntimeError("Method call requires object instance")

    def eval_new_instance(self, node: n.NewInstance) -> MiniInstance:
        klass = self.classes.get(node.class_name)
        if not klass:
            raise RuntimeError(f"Class not found: {node.class_name}")
        instance = MiniInstance(klass, dict(klass.fields))
        ctor = klass.methods.get("constructor") or klass.methods.get(node.class_name)
        if ctor:
            self._call_method(instance, ctor, [self.eval(a) for a in node.arguments])
        return instance

    def eval_property_access(self, node: n.PropertyAccess) -> Any:
        receiver = self.eval(node.receiver)
        if isinstance(receiver, MiniInstance):
            if node.property_name in receiver.fields:
                return receiver.fields[node.property_name]
            raise RuntimeError(
                f"Property '{node.property_name}' not found on {receiver.klass.name}"
            )
        raise RuntimeError("Property access requires object instance")

    def _call_function(self, fn: MiniFunction, args: List[Any]) -> Any:
        env = Environment(fn.closure)
        for param, arg in zip(fn.parameters, args):
            env.define(param.name, arg)
        old = self.env
        self.env = env
        try:
            try:
                self.exec_block(fn.body)
            except ReturnSignal as sig:
                return sig.value
            return None
        finally:
            self.env = old

    def _call_method(
        self, instance: MiniInstance, method: n.MethodDecl, args: List[Any]
    ) -> Any:
        env = Environment(self.globals)
        env.define("this", instance)
        for param, arg in zip(method.parameters, args):
            env.define(param.name, arg)
        old_env = self.env
        old_this = self.this_instance
        self.env = env
        self.this_instance = instance
        try:
            try:
                self.exec_block(method.body)
            except ReturnSignal as sig:
                return sig.value
            return None
        finally:
            self.env = old_env
            self.this_instance = old_this

    @staticmethod
    def _truthy(value: Any) -> bool:
        return bool(value)

    @staticmethod
    def _format_value(value: Any) -> str:
        if isinstance(value, float) and value == int(value):
            return str(int(value))
        return str(value)


def _par_worker(stmt_data: bytes, shared_data: bytes, port: int, channels: Dict) -> None:
    """Isolated process for exec_par — executes one statement, sends output+env via TCP."""
    import json
    import pickle
    import socket

    shared = pickle.loads(shared_data)
    stmt = pickle.loads(stmt_data)

    child = Interpreter()
    child.classes = shared["classes"]
    for name, klass in child.classes.items():
        child.globals.define(name, klass)
    for k, v in shared["env"].items():
        child.globals.define(k, v)
    child._channels = channels  # shared multiprocessing.Queue objects

    output_lines: List[str] = []
    child._print_hook = lambda txt: output_lines.append(txt)

    # Track new env definitions (e.g. receive(ch, result) creates result)
    env_updates: Dict[str, Any] = {}
    _orig_define = child.env.define

    def _tracking_define(name: str, value: Any) -> None:
        if isinstance(value, (str, int, float, bool, type(None))):
            env_updates[name] = value
        _orig_define(name, value)

    child.env.define = _tracking_define  # type: ignore[method-assign]

    try:
        child.exec(stmt)
    except Exception:
        pass

    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    conn.connect(("127.0.0.1", port))
    conn.sendall(json.dumps({"output": output_lines, "env": env_updates}).encode() + b"\n")
    conn.close()


class InterpreterBackend(AbstractBackendTranslator):
    def __init__(self) -> None:
        self._interpreter: Interpreter | None = None
        self._output = ""
        self._runtime_errors: list[str] = []

    def emit(self, ast_dict: dict) -> None:
        program = from_dict(ast_dict)
        if not isinstance(program, n.Program):
            raise TypeError("Expected Program")
        interp = Interpreter()
        try:
            self._output = interp.execute(program)
        except RuntimeError as exc:
            self._runtime_errors.append(str(exc))

    def finalize(self) -> TranslationResult:
        if self._runtime_errors:
            return TranslationResult(
                output="; ".join(self._runtime_errors),
                exit_code=1,
                errors=list(self._runtime_errors),
            )
        return TranslationResult(output=self._output, exit_code=0)


def interpret_ast(ast_dict: dict) -> TranslationResult:
    return InterpreterBackend().translate(ast_dict)
