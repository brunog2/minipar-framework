"""Análise semântica MiniPar 2026.1 — MVP OO + procedural."""

from typing import List, Optional

from minipar_core import ast_nodes as n
from minipar_core.symbol_table import SymbolTable, SymbolType


class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[str] = []
        self.current_function_return_type: Optional[str] = None
        self.current_class: Optional[str] = None
        self.in_loop = False
        self.known_classes: dict[str, Optional[str]] = {}
        self._init_builtins()

    def _init_builtins(self):
        builtins = [
            ("print", "void", ["any"]),
            ("println", "void", ["any"]),
            ("input", "any", ["string"]),
            ("len", "number", ["any"]),
        ]
        for name, return_type, param_types in builtins:
            self.symbol_table.add_symbol(
                name,
                SymbolType.FUNCTION,
                return_type,
                line=0,
                param_types=param_types,
                return_type=return_type,
            )

    def add_error(self, message: str, line: int = 0):
        self.errors.append(f"Semantic error at line {line}: {message}")

    def analyze(self, node: n.ASTNode) -> bool:
        self.errors = []
        self.visit(node)
        return len(self.errors) == 0

    def visit(self, node: n.ASTNode):
        if node is None:
            return None
        method = getattr(self, f"visit_{type(node).__name__}", None)
        if method is None:
            return None
        return method(node)

    def is_type_compatible(self, expected: str, actual: Optional[str]) -> bool:
        if actual is None or expected is None:
            return True
        if expected == actual or expected == "any" or actual == "any":
            return True
        return False

    def visit_Program(self, node: n.Program):
        for decl in node.declarations:
            self.visit(decl)

    def visit_ClassDecl(self, node: n.ClassDecl):
        if node.name in self.known_classes:
            self.add_error(f"Class '{node.name}' already declared")
            return
        if node.extends and node.extends not in self.known_classes:
            self.add_error(f"Superclass '{node.extends}' not found for class '{node.name}'")
        self.known_classes[node.name] = node.extends
        self.symbol_table.add_symbol(
            node.name, SymbolType.CLASS, node.name, line=node.line, parent_class=node.extends
        )
        self.symbol_table.enter_scope(f"class_{node.name}")
        self.current_class = node.name
        seen_members: set[str] = set()
        for member in node.members:
            if isinstance(member, n.VarDecl):
                if member.name in seen_members:
                    self.add_error(f"Duplicate member '{member.name}' in class '{node.name}'")
                seen_members.add(member.name)
                self.symbol_table.add_symbol(
                    member.name,
                    SymbolType.ATTRIBUTE,
                    member.var_type,
                    line=member.line,
                    parent_class=node.name,
                )
                if member.initializer:
                    self.visit(member.initializer)
            elif isinstance(member, n.MethodDecl):
                if member.name in seen_members:
                    self.add_error(f"Duplicate member '{member.name}' in class '{node.name}'")
                seen_members.add(member.name)
                self.symbol_table.add_symbol(
                    member.name,
                    SymbolType.METHOD,
                    member.return_type,
                    line=member.line,
                    parent_class=node.name,
                    param_types=[p.param_type for p in member.parameters],
                    return_type=member.return_type,
                )
                self.symbol_table.enter_scope(f"method_{member.name}")
                for param in member.parameters:
                    self.symbol_table.add_symbol(
                        param.name,
                        SymbolType.PARAMETER,
                        param.param_type,
                        line=param.line,
                        parent_class=node.name,
                    )
                old_ret = self.current_function_return_type
                self.current_function_return_type = member.return_type
                self.visit(member.body)
                self.current_function_return_type = old_ret
                self.symbol_table.exit_scope()
        self.current_class = None
        self.symbol_table.exit_scope()

    def visit_VarDecl(self, node: n.VarDecl):
        if self.symbol_table.lookup_local(node.name):
            self.add_error(f"Variable '{node.name}' already declared in current scope", node.line)
            return
        if node.initializer:
            self.visit(node.initializer)
        self.symbol_table.add_symbol(
            node.name, SymbolType.VARIABLE, node.var_type, line=node.line, is_initialized=node.initializer is not None
        )

    def visit_FuncDecl(self, node: n.FuncDecl):
        if self.symbol_table.lookup_local(node.name):
            self.add_error(f"Function '{node.name}' already declared", node.line)
            return
        param_types = [p.var_type for p in node.parameters]
        self.symbol_table.add_symbol(
            node.name,
            SymbolType.FUNCTION,
            node.return_type,
            line=node.line,
            param_types=param_types,
            return_type=node.return_type,
        )
        self.symbol_table.enter_scope(f"func_{node.name}")
        for param in node.parameters:
            self.symbol_table.add_symbol(
                param.name, SymbolType.PARAMETER, param.var_type, line=param.line
            )
        old_ret = self.current_function_return_type
        self.current_function_return_type = node.return_type
        self.visit(node.body)
        self.current_function_return_type = old_ret
        self.symbol_table.exit_scope()

    def visit_ChannelDecl(self, node: n.ChannelDecl):
        if self.symbol_table.lookup_local(node.name):
            self.add_error(f"Channel '{node.name}' already declared", node.line)
            return
        self.symbol_table.add_symbol(
            node.name, SymbolType.CHANNEL, node.channel_type, line=node.line, channel_type=node.channel_type
        )
        for arg in node.arguments:
            self.visit(arg)

    def visit_Block(self, node: n.Block):
        self.symbol_table.enter_scope("block")
        for stmt in node.statements:
            self.visit(stmt)
        self.symbol_table.exit_scope()

    def visit_SeqBlock(self, node: n.SeqBlock):
        self.symbol_table.enter_scope("seq")
        for stmt in node.statements:
            self.visit(stmt)
        self.symbol_table.exit_scope()

    def visit_ParBlock(self, node: n.ParBlock):
        self.symbol_table.enter_scope("par")
        for stmt in node.statements:
            self.visit(stmt)
        self.symbol_table.exit_scope()

    def visit_IfStmt(self, node: n.IfStmt):
        self.visit(node.condition)
        self.visit(node.then_branch)
        if node.else_branch:
            self.visit(node.else_branch)

    def visit_WhileStmt(self, node: n.WhileStmt):
        self.visit(node.condition)
        old = self.in_loop
        self.in_loop = True
        self.visit(node.body)
        self.in_loop = old

    def visit_ForStmt(self, node: n.ForStmt):
        self.symbol_table.enter_scope("for")
        self.symbol_table.add_symbol(node.variable.name, SymbolType.VARIABLE, node.variable.var_type, line=node.line)
        self.visit(node.iterable)
        old = self.in_loop
        self.in_loop = True
        self.visit(node.body)
        self.in_loop = old
        self.symbol_table.exit_scope()

    def visit_ReturnStmt(self, node: n.ReturnStmt):
        if self.current_function_return_type is None:
            self.add_error("Return statement outside function/method", node.line)
            return
        if node.value:
            self.visit(node.value)

    def visit_BreakStmt(self, node: n.BreakStmt):
        if not self.in_loop:
            self.add_error("Break outside loop", node.line)

    def visit_ContinueStmt(self, node: n.ContinueStmt):
        if not self.in_loop:
            self.add_error("Continue outside loop", node.line)

    def visit_PrintStmt(self, node: n.PrintStmt):
        for arg in node.arguments:
            self.visit(arg)

    def visit_ExprStmt(self, node: n.ExprStmt):
        self.visit(node.expression)

    def visit_Assignment(self, node: n.Assignment):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.add_error(f"Undefined variable '{node.name}'", node.line)
        self.visit(node.value)

    def visit_PropertyAssign(self, node: n.PropertyAssign):
        self.visit(node.receiver)
        self.visit(node.value)

    def visit_BinaryOp(self, node: n.BinaryOp):
        self.visit(node.left)
        self.visit(node.right)
        return "number"

    def visit_UnaryOp(self, node: n.UnaryOp):
        self.visit(node.operand)
        return "number"

    def visit_FuncCall(self, node: n.FuncCall):
        sym = self.symbol_table.lookup(node.name)
        if not sym:
            self.add_error(f"Undefined function '{node.name}'", node.line)
        for arg in node.arguments:
            self.visit(arg)
        return sym.return_type if sym else "any"

    def visit_MethodCall(self, node: n.MethodCall):
        self.visit(node.receiver)
        for arg in node.arguments:
            self.visit(arg)
        return "any"

    def visit_PropertyAccess(self, node: n.PropertyAccess):
        self.visit(node.receiver)
        return "any"

    def visit_Variable(self, node: n.Variable):
        sym = self.symbol_table.lookup(node.name)
        if not sym and node.name not in self.known_classes:
            self.add_error(f"Undefined identifier '{node.name}'", node.line)
            return "any"
        if node.name in self.known_classes:
            return node.name
        return sym.data_type if sym else "any"

    def visit_ThisExpr(self, node: n.ThisExpr):
        if not self.current_class:
            self.add_error("'this' used outside class", node.line)
        return self.current_class or "any"

    def visit_SuperCall(self, node: n.SuperCall):
        if not self.current_class:
            self.add_error("'super' used outside class", node.line)
        for arg in node.arguments:
            self.visit(arg)

    def visit_NewInstance(self, node: n.NewInstance):
        if node.class_name not in self.known_classes:
            self.add_error(f"Unknown class '{node.class_name}'", node.line)
        for arg in node.arguments:
            self.visit(arg)
        return node.class_name

    def visit_NumberLiteral(self, node: n.NumberLiteral):
        return "number"

    def visit_StringLiteral(self, node: n.StringLiteral):
        return "string"

    def visit_BoolLiteral(self, node: n.BoolLiteral):
        return "bool"

    def visit_ListLiteral(self, node: n.ListLiteral):
        for el in node.elements:
            self.visit(el)
        return "list"

    def visit_ListComprehension(self, node: n.ListComprehension):
        self.visit(node.iterable)
        self.visit(node.expression)
        return "list"

    def visit_DictLiteral(self, node: n.DictLiteral):
        for key, value in node.pairs:
            self.visit(key)
            self.visit(value)
        return "dict"

    def visit_IndexAccess(self, node: n.IndexAccess):
        self.visit(node.object)
        self.visit(node.index)
        return "any"

    def visit_SliceAccess(self, node: n.SliceAccess):
        self.visit(node.object)
        if node.start:
            self.visit(node.start)
        if node.end:
            self.visit(node.end)
        return "any"
