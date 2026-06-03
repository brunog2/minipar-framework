"""Serialização AST → JSON conforme microservices/_AST_CONTRACT.md."""

from minipar_core import ast_nodes as n


def to_dict(node) -> dict | list | str | int | float | bool | None:
    if node is None:
        return None
    if isinstance(node, bool):
        return node
    if isinstance(node, (int, float, str)):
        return node
    if isinstance(node, list):
        return [to_dict(x) for x in node]
    if isinstance(node, tuple):
        return [to_dict(node[0]), to_dict(node[1])]

    if isinstance(node, n.Program):
        return {"type": "Program", "declarations": to_dict(node.declarations)}

    if isinstance(node, n.ClassDecl):
        return {
            "type": "ClassDecl",
            "name": node.name,
            "extends": node.extends,
            "members": to_dict(node.members),
        }

    if isinstance(node, n.MethodDecl):
        return {
            "type": "MethodDecl",
            "name": node.name,
            "returnType": node.return_type,
            "isConstructor": node.is_constructor,
            "parameters": to_dict(node.parameters),
            "body": to_dict(node.body),
        }

    if isinstance(node, n.Parameter):
        return {"type": "Parameter", "name": node.name, "paramType": node.param_type}

    if isinstance(node, n.VarDecl):
        return {
            "type": "VarDecl",
            "name": node.name,
            "varType": node.var_type,
            "initializer": to_dict(node.initializer),
        }

    if isinstance(node, n.FuncDecl):
        return {
            "type": "FuncDecl",
            "name": node.name,
            "returnType": node.return_type,
            "parameters": to_dict(node.parameters),
            "body": to_dict(node.body),
        }

    if isinstance(node, n.Block):
        return {"type": "Block", "statements": to_dict(node.statements)}

    if isinstance(node, n.ParBlock):
        return {"type": "ParBlock", "statements": to_dict(node.statements)}

    if isinstance(node, n.SeqBlock):
        return {"type": "SeqBlock", "statements": to_dict(node.statements)}

    if isinstance(node, n.PrintStmt):
        return {
            "type": "PrintStmt",
            "newline": node.newline,
            "arguments": to_dict(node.arguments),
        }

    if isinstance(node, n.NewInstance):
        return {
            "type": "NewInstance",
            "className": node.class_name,
            "arguments": to_dict(node.arguments),
        }

    if isinstance(node, n.MethodCall):
        return {
            "type": "MethodCall",
            "method": node.method,
            "receiver": to_dict(node.receiver),
            "arguments": to_dict(node.arguments),
        }

    if isinstance(node, n.PropertyAccess):
        return {
            "type": "PropertyAccess",
            "property": node.property_name,
            "receiver": to_dict(node.receiver),
        }

    if isinstance(node, n.ThisExpr):
        return {"type": "ThisExpr"}

    if isinstance(node, n.SuperCall):
        return {"type": "SuperCall", "arguments": to_dict(node.arguments)}

    if isinstance(node, n.IfStmt):
        return {
            "type": "IfStmt",
            "condition": to_dict(node.condition),
            "thenBranch": to_dict(node.then_branch),
            "elseBranch": to_dict(node.else_branch),
        }

    if isinstance(node, n.WhileStmt):
        return {"type": "WhileStmt", "condition": to_dict(node.condition), "body": to_dict(node.body)}

    if isinstance(node, n.ForStmt):
        return {
            "type": "ForStmt",
            "variable": to_dict(node.variable),
            "iterable": to_dict(node.iterable),
            "body": to_dict(node.body),
        }

    if isinstance(node, n.ReturnStmt):
        return {"type": "ReturnStmt", "value": to_dict(node.value)}

    if isinstance(node, n.BreakStmt):
        return {"type": "BreakStmt"}

    if isinstance(node, n.ContinueStmt):
        return {"type": "ContinueStmt"}

    if isinstance(node, n.ExprStmt):
        return {"type": "ExprStmt", "expression": to_dict(node.expression)}

    if isinstance(node, n.Assignment):
        return {"type": "Assignment", "name": node.name, "value": to_dict(node.value)}

    if isinstance(node, n.PropertyAssign):
        return {
            "type": "PropertyAssign",
            "property": node.property_name,
            "receiver": to_dict(node.receiver),
            "value": to_dict(node.value),
        }

    if isinstance(node, n.BinaryOp):
        return {
            "type": "BinaryOp",
            "operator": node.operator,
            "left": to_dict(node.left),
            "right": to_dict(node.right),
        }

    if isinstance(node, n.UnaryOp):
        return {"type": "UnaryOp", "operator": node.operator, "operand": to_dict(node.operand)}

    if isinstance(node, n.FuncCall):
        return {"type": "FuncCall", "name": node.name, "arguments": to_dict(node.arguments)}

    if isinstance(node, n.Variable):
        return {"type": "Variable", "name": node.name}

    if isinstance(node, n.NumberLiteral):
        return {"type": "NumberLiteral", "value": node.value}

    if isinstance(node, n.StringLiteral):
        return {"type": "StringLiteral", "value": node.value}

    if isinstance(node, n.BoolLiteral):
        return {"type": "BoolLiteral", "value": node.value}

    if isinstance(node, n.ListLiteral):
        return {"type": "ListLiteral", "elements": to_dict(node.elements)}

    if isinstance(node, n.ListComprehension):
        return {
            "type": "ListComprehension",
            "variable": to_dict(node.variable),
            "iterable": to_dict(node.iterable),
            "expression": to_dict(node.expression),
        }

    if isinstance(node, n.DictLiteral):
        return {"type": "DictLiteral", "pairs": to_dict(node.pairs)}

    if isinstance(node, n.ChannelDecl):
        return {
            "type": "ChannelDecl",
            "channelType": node.channel_type,
            "name": node.name,
            "arguments": to_dict(node.arguments),
        }

    if isinstance(node, n.IndexAccess):
        return {
            "type": "IndexAccess",
            "object": to_dict(node.object),
            "index": to_dict(node.index),
        }

    if isinstance(node, n.SliceAccess):
        return {
            "type": "SliceAccess",
            "object": to_dict(node.object),
            "start": to_dict(node.start),
            "end": to_dict(node.end),
        }

    if isinstance(node, n.SendStmt):
        return {"type": "SendStmt", "channel": node.channel, "value": to_dict(node.value)}

    if isinstance(node, n.ReceiveStmt):
        return {"type": "ReceiveStmt", "channel": node.channel, "target": node.target}

    raise TypeError(f"Unknown AST node: {type(node).__name__}")
