"""Gerador TAC a partir da AST MiniPar 2026.1 (procedural + OO MVP)."""

from __future__ import annotations

from typing import List, Optional

from minipar_core import ast_nodes as n
from minipar_core.translation.tac import TAC


class TACGenerator:
    def __init__(self) -> None:
        self.code: List[TAC] = []
        self.temp_count = 0
        self.label_count = 0
        self.loop_stack: List[tuple[str, str]] = []
        self.class_stack: List[str] = []

    def new_temp(self) -> str:
        name = f"t{self.temp_count}"
        self.temp_count += 1
        return name

    def new_label(self) -> str:
        name = f"L{self.label_count}"
        self.label_count += 1
        return name

    def emit(self, op: str, arg1=None, arg2=None, result=None) -> None:
        self.code.append(TAC(op, arg1, arg2, result))

    def generate(self, node) -> Optional[str]:
        method = getattr(self, f"gen_{node.__class__.__name__}", None)
        if method is None:
            raise NotImplementedError(
                f"TAC generation not implemented for {node.__class__.__name__}"
            )
        return method(node)

    def gen_Program(self, node: n.Program) -> None:
        for decl in node.declarations:
            self.generate(decl)
        self.emit("CALL_MAIN")

    def gen_ClassDecl(self, node: n.ClassDecl) -> None:
        self.class_stack.append(node.name)
        for member in node.members:
            self.generate(member)
        self.class_stack.pop()

    def gen_MethodDecl(self, node: n.MethodDecl) -> None:
        class_name = self.class_stack[-1] if self.class_stack else "Global"
        fn_name = f"{class_name}_{node.name}"
        self.emit("FUNC_BEGIN", fn_name)
        for param in node.parameters:
            self.emit("PARAM", param.name)
        self.generate(node.body)
        self.emit("FUNC_END", fn_name)

    def gen_VarDecl(self, node: n.VarDecl) -> None:
        if node.initializer:
            value = self.generate(node.initializer)
            self.emit("ASSIGN", value, None, node.name)

    def gen_FuncDecl(self, node: n.FuncDecl) -> None:
        self.emit("FUNC_BEGIN", node.name)
        for param in node.parameters:
            self.emit("PARAM", param.name)
        self.generate(node.body)
        self.emit("FUNC_END", node.name)

    def gen_Block(self, node: n.Block) -> None:
        for stmt in node.statements:
            self.generate(stmt)

    def gen_PrintStmt(self, node: n.PrintStmt) -> None:
        for arg in node.arguments:
            value = self.generate(arg)
            self.emit("PRINT", value, "1" if node.newline else "0")

    def gen_IfStmt(self, node: n.IfStmt) -> None:
        condition = self.generate(node.condition)
        else_label = self.new_label()
        end_label = self.new_label()
        if node.else_branch:
            self.emit("IF_FALSE", condition, None, else_label)
            self.generate(node.then_branch)
            self.emit("GOTO", end_label)
            self.emit("LABEL", else_label)
            self.generate(node.else_branch)
            self.emit("LABEL", end_label)
        else:
            self.emit("IF_FALSE", condition, None, else_label)
            self.generate(node.then_branch)
            self.emit("LABEL", else_label)

    def gen_WhileStmt(self, node: n.WhileStmt) -> None:
        start = self.new_label()
        end = self.new_label()
        self.loop_stack.append((start, end))
        self.emit("LABEL", start)
        cond = self.generate(node.condition)
        self.emit("IF_FALSE", cond, None, end)
        self.generate(node.body)
        self.emit("GOTO", start)
        self.emit("LABEL", end)
        self.loop_stack.pop()

    def gen_ForStmt(self, node: n.ForStmt) -> None:
        start = self.new_label()
        end = self.new_label()
        self.loop_stack.append((start, end))
        iterable = self.generate(node.iterable)
        index_var = self.new_temp()
        length_var = self.new_temp()
        self.emit("LIST_LEN", iterable, None, length_var)
        self.emit("ASSIGN", 0, None, index_var)
        self.emit("LABEL", start)
        cond = self.new_temp()
        self.emit("LT", index_var, length_var, cond)
        self.emit("IF_FALSE", cond, None, end)
        self.emit("LIST_GET", iterable, index_var, node.variable.name)
        self.generate(node.body)
        inc = self.new_temp()
        self.emit("ADD", index_var, 1, inc)
        self.emit("ASSIGN", inc, None, index_var)
        self.emit("GOTO", start)
        self.emit("LABEL", end)
        self.loop_stack.pop()

    def gen_ReturnStmt(self, node: n.ReturnStmt) -> None:
        if node.value:
            self.emit("RETURN", self.generate(node.value))
        else:
            self.emit("RETURN")

    def gen_BreakStmt(self, node: n.BreakStmt) -> None:
        if not self.loop_stack:
            raise RuntimeError("Break outside loop")
        self.emit("GOTO", self.loop_stack[-1][1])

    def gen_ContinueStmt(self, node: n.ContinueStmt) -> None:
        if not self.loop_stack:
            raise RuntimeError("Continue outside loop")
        self.emit("GOTO", self.loop_stack[-1][0])

    def gen_ExprStmt(self, node: n.ExprStmt) -> None:
        self.generate(node.expression)

    def gen_Assignment(self, node: n.Assignment) -> str:
        value = self.generate(node.value)
        self.emit("ASSIGN", value, None, node.name)
        return node.name

    def gen_BinaryOp(self, node: n.BinaryOp) -> str:
        left = self.generate(node.left)
        right = self.generate(node.right)
        result = self.new_temp()
        self.emit(node.operator, left, right, result)
        return result

    def gen_UnaryOp(self, node: n.UnaryOp) -> str:
        operand = self.generate(node.operand)
        result = self.new_temp()
        self.emit("UNARY", node.operator, operand, result)
        return result

    def gen_FuncCall(self, node: n.FuncCall) -> str:
        for arg in node.arguments:
            self.emit("PARAM", self.generate(arg))
        result = self.new_temp()
        self.emit("CALL", node.name, len(node.arguments), result)
        return result

    def gen_MethodCall(self, node: n.MethodCall) -> str:
        receiver = self.generate(node.receiver)
        for arg in node.arguments:
            self.emit("PARAM", self.generate(arg))
        result = self.new_temp()
        self.emit("METHOD_CALL", receiver, node.method, result)
        self.emit("METHOD_ARGS", len(node.arguments))
        return result

    def gen_NewInstance(self, node: n.NewInstance) -> str:
        for arg in node.arguments:
            self.emit("PARAM", self.generate(arg))
        result = self.new_temp()
        self.emit("NEW", node.class_name, len(node.arguments), result)
        return result

    def gen_PropertyAccess(self, node: n.PropertyAccess) -> str:
        receiver = self.generate(node.receiver)
        result = self.new_temp()
        self.emit("GET_PROP", receiver, node.property_name, result)
        return result

    def gen_PropertyAssign(self, node: n.PropertyAssign) -> None:
        receiver = self.generate(node.receiver)
        value = self.generate(node.value)
        self.emit("SET_PROP", receiver, node.property_name, value)

    def gen_Variable(self, node: n.Variable) -> str:
        return node.name

    def gen_ThisExpr(self, node: n.ThisExpr) -> str:
        return "this"

    def gen_NumberLiteral(self, node: n.NumberLiteral) -> str:
        return str(node.value)

    def gen_StringLiteral(self, node: n.StringLiteral) -> str:
        return f'"{node.value}"'

    def gen_BoolLiteral(self, node: n.BoolLiteral) -> str:
        return "1" if node.value else "0"

    def gen_ListLiteral(self, node: n.ListLiteral) -> str:
        result = self.new_temp()
        self.emit("LIST_CREATE", None, None, result)
        for elem in node.elements:
            self.emit("LIST_APPEND", result, self.generate(elem))
        return result

    def gen_DictLiteral(self, node: n.DictLiteral) -> str:
        result = self.new_temp()
        self.emit("DICT_CREATE", None, None, result)
        for key, value in node.pairs:
            self.emit("DICT_SET", result, self.generate(key), self.generate(value))
        return result

    def gen_SeqBlock(self, node: n.SeqBlock) -> None:
        self.emit("SEQ_BEGIN")
        for stmt in node.statements:
            self.generate(stmt)
        self.emit("SEQ_END")

    def gen_ParBlock(self, node: n.ParBlock) -> None:
        self.emit("PAR_BEGIN")
        for i, stmt in enumerate(node.statements):
            self.emit("THREAD_START", i)
            self.generate(stmt)
            self.emit("THREAD_END", i)
        self.emit("PAR_END")

    def gen_ChannelDecl(self, node: n.ChannelDecl) -> None:
        args = ",".join(str(self.generate(a)) for a in node.arguments)
        self.emit("CHANNEL_CREATE", node.channel_type, node.name, args)

    def gen_IndexAccess(self, node: n.IndexAccess) -> str:
        obj = self.generate(node.object)
        idx = self.generate(node.index)
        result = self.new_temp()
        self.emit("INDEX", obj, idx, result)
        return result

    def lower(self, ast_dict: dict) -> List[TAC]:
        from minipar_core.translation.ast_from_json import from_dict

        program = from_dict(ast_dict)
        if not isinstance(program, n.Program):
            raise TypeError("Expected Program AST")
        self.code = []
        self.generate(program)
        return self.code
