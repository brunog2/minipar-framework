"""Deserialização JSON → nós AST (espelho de ast_json.to_dict)."""

from minipar_core import ast_nodes as n


def from_dict(data: dict | list | str | int | float | bool | None):
    if data is None:
        return None
    if isinstance(data, bool):
        return data
    if isinstance(data, (int, float, str)):
        return data
    if isinstance(data, list):
        return [from_dict(x) for x in data]

    if not isinstance(data, dict):
        raise TypeError(f"Expected dict AST node, got {type(data)}")

    node_type = data.get("type")
    if node_type == "Program":
        return n.Program(declarations=from_dict(data["declarations"]))

    if node_type == "ClassDecl":
        return n.ClassDecl(
            name=data["name"],
            extends=data.get("extends"),
            members=from_dict(data.get("members", [])),
        )

    if node_type == "MethodDecl":
        return n.MethodDecl(
            return_type=data["returnType"],
            name=data["name"],
            parameters=from_dict(data.get("parameters", [])),
            body=from_dict(data["body"]),
            is_constructor=data.get("isConstructor", False),
        )

    if node_type == "Parameter":
        return n.Parameter(name=data["name"], param_type=data["paramType"])

    if node_type == "VarDecl":
        return n.VarDecl(
            var_type=data["varType"],
            name=data["name"],
            initializer=from_dict(data.get("initializer")),
        )

    if node_type == "FuncDecl":
        return n.FuncDecl(
            return_type=data["returnType"],
            name=data["name"],
            parameters=from_dict(data.get("parameters", [])),
            body=from_dict(data["body"]),
        )

    if node_type == "Block":
        return n.Block(statements=from_dict(data.get("statements", [])))

    if node_type == "ParBlock":
        return n.ParBlock(statements=from_dict(data.get("statements", [])))

    if node_type == "SeqBlock":
        return n.SeqBlock(statements=from_dict(data.get("statements", [])))

    if node_type == "PrintStmt":
        return n.PrintStmt(
            arguments=from_dict(data.get("arguments", [])),
            newline=data.get("newline", False),
        )

    if node_type == "NewInstance":
        return n.NewInstance(
            class_name=data["className"],
            arguments=from_dict(data.get("arguments", [])),
        )

    if node_type == "MethodCall":
        return n.MethodCall(
            method=data["method"],
            receiver=from_dict(data["receiver"]),
            arguments=from_dict(data.get("arguments", [])),
        )

    if node_type == "PropertyAccess":
        return n.PropertyAccess(
            property_name=data["property"],
            receiver=from_dict(data["receiver"]),
        )

    if node_type == "ThisExpr":
        return n.ThisExpr()

    if node_type == "SuperCall":
        return n.SuperCall(arguments=from_dict(data.get("arguments", [])))

    if node_type == "IfStmt":
        return n.IfStmt(
            condition=from_dict(data["condition"]),
            then_branch=from_dict(data["thenBranch"]),
            else_branch=from_dict(data.get("elseBranch")),
        )

    if node_type == "WhileStmt":
        return n.WhileStmt(
            condition=from_dict(data["condition"]),
            body=from_dict(data["body"]),
        )

    if node_type == "ForStmt":
        return n.ForStmt(
            variable=from_dict(data["variable"]),
            iterable=from_dict(data["iterable"]),
            body=from_dict(data["body"]),
        )

    if node_type == "ReturnStmt":
        return n.ReturnStmt(value=from_dict(data.get("value")))

    if node_type == "BreakStmt":
        return n.BreakStmt()

    if node_type == "ContinueStmt":
        return n.ContinueStmt()

    if node_type == "ExprStmt":
        return n.ExprStmt(expression=from_dict(data["expression"]))

    if node_type == "Assignment":
        return n.Assignment(name=data["name"], value=from_dict(data["value"]))

    if node_type == "PropertyAssign":
        return n.PropertyAssign(
            property_name=data["property"],
            receiver=from_dict(data["receiver"]),
            value=from_dict(data["value"]),
        )

    if node_type == "BinaryOp":
        return n.BinaryOp(
            operator=data["operator"],
            left=from_dict(data["left"]),
            right=from_dict(data["right"]),
        )

    if node_type == "UnaryOp":
        return n.UnaryOp(
            operator=data["operator"],
            operand=from_dict(data["operand"]),
        )

    if node_type == "FuncCall":
        return n.FuncCall(
            name=data["name"],
            arguments=from_dict(data.get("arguments", [])),
        )

    if node_type == "Variable":
        return n.Variable(name=data["name"])

    if node_type == "NumberLiteral":
        return n.NumberLiteral(value=data["value"])

    if node_type == "StringLiteral":
        return n.StringLiteral(value=data["value"])

    if node_type == "BoolLiteral":
        return n.BoolLiteral(value=data["value"])

    if node_type == "ListLiteral":
        return n.ListLiteral(elements=from_dict(data.get("elements", [])))

    if node_type == "ListComprehension":
        return n.ListComprehension(
            variable=from_dict(data["variable"]),
            iterable=from_dict(data["iterable"]),
            expression=from_dict(data["expression"]),
        )

    if node_type == "DictLiteral":
        pairs = []
        for item in data.get("pairs", []):
            if isinstance(item, list) and len(item) == 2:
                pairs.append((from_dict(item[0]), from_dict(item[1])))
        return n.DictLiteral(pairs=pairs)

    if node_type == "ChannelDecl":
        return n.ChannelDecl(
            channel_type=data["channelType"],
            name=data["name"],
            arguments=from_dict(data.get("arguments", [])),
        )

    if node_type == "IndexAccess":
        return n.IndexAccess(
            object=from_dict(data["object"]),
            index=from_dict(data["index"]),
        )

    if node_type == "SliceAccess":
        return n.SliceAccess(
            object=from_dict(data["object"]),
            start=from_dict(data.get("start")),
            end=from_dict(data.get("end")),
        )

    raise TypeError(f"Unknown AST node type: {node_type}")
