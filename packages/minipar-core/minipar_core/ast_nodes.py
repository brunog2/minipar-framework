"""Nós da AST MiniPar 2026.1 — procedural + OO."""

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ASTNode:
    pass


@dataclass
class Program(ASTNode):
    declarations: List[ASTNode]


@dataclass
class ClassDecl(ASTNode):
    name: str
    extends: Optional[str]
    members: List[ASTNode] = field(default_factory=list)


@dataclass
class MethodDecl(ASTNode):
    return_type: str
    name: str
    parameters: List["Parameter"]
    body: "Block"
    is_constructor: bool = False


@dataclass
class Parameter(ASTNode):
    name: str
    param_type: str


@dataclass
class VarDecl(ASTNode):
    var_type: str
    name: str
    initializer: Optional[ASTNode] = None


@dataclass
class FuncDecl(ASTNode):
    return_type: str
    name: str
    parameters: List[VarDecl]
    body: "Block"


@dataclass
class Block(ASTNode):
    statements: List[ASTNode]


@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    then_branch: ASTNode
    else_branch: Optional[ASTNode] = None


@dataclass
class WhileStmt(ASTNode):
    condition: ASTNode
    body: ASTNode


@dataclass
class ForStmt(ASTNode):
    variable: VarDecl
    iterable: ASTNode
    body: ASTNode


@dataclass
class ReturnStmt(ASTNode):
    value: Optional[ASTNode] = None


@dataclass
class BreakStmt(ASTNode):
    pass


@dataclass
class ContinueStmt(ASTNode):
    pass


@dataclass
class PrintStmt(ASTNode):
    arguments: List[ASTNode]
    newline: bool = False


@dataclass
class ExprStmt(ASTNode):
    expression: ASTNode


@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode


@dataclass
class PropertyAssign(ASTNode):
    receiver: ASTNode
    property_name: str
    value: ASTNode


@dataclass
class BinaryOp(ASTNode):
    left: ASTNode
    operator: str
    right: ASTNode


@dataclass
class UnaryOp(ASTNode):
    operator: str
    operand: ASTNode


@dataclass
class FuncCall(ASTNode):
    name: str
    arguments: List[ASTNode]


@dataclass
class MethodCall(ASTNode):
    receiver: ASTNode
    method: str
    arguments: List[ASTNode]


@dataclass
class PropertyAccess(ASTNode):
    receiver: ASTNode
    property_name: str


@dataclass
class Variable(ASTNode):
    name: str


@dataclass
class ThisExpr(ASTNode):
    pass


@dataclass
class SuperCall(ASTNode):
    arguments: List[ASTNode]


@dataclass
class NewInstance(ASTNode):
    class_name: str
    arguments: List[ASTNode]


@dataclass
class NumberLiteral(ASTNode):
    value: float


@dataclass
class StringLiteral(ASTNode):
    value: str


@dataclass
class BoolLiteral(ASTNode):
    value: bool


@dataclass
class ListLiteral(ASTNode):
    elements: List[ASTNode]


@dataclass
class ListComprehension(ASTNode):
    variable: VarDecl
    iterable: ASTNode
    expression: ASTNode


@dataclass
class DictLiteral(ASTNode):
    pairs: List[tuple]


@dataclass
class ChannelDecl(ASTNode):
    channel_type: str
    name: str
    arguments: List[ASTNode]


@dataclass
class SeqBlock(ASTNode):
    statements: List[ASTNode]


@dataclass
class ParBlock(ASTNode):
    statements: List[ASTNode]


@dataclass
class IndexAccess(ASTNode):
    object: ASTNode
    index: ASTNode


@dataclass
class SliceAccess(ASTNode):
    object: ASTNode
    start: Optional[ASTNode] = None
    end: Optional[ASTNode] = None


@dataclass
class SendStmt(ASTNode):
    channel: str
    value: ASTNode


@dataclass
class ReceiveStmt(ASTNode):
    channel: str
    target: str
