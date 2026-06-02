"""Análise semântica sobre AST JSON (contrato REST do ms-semantic)."""

from typing import Any


def analyze_ast_dict(ast: dict) -> tuple[dict, dict, list[str]]:
    errors: list[str] = []
    known_classes: dict[str, str | None] = {}
    scopes: list[dict] = [{"name": "global", "level": 0, "symbols": []}]

    def add_symbol(name: str, kind: str, data_type: str, parent_class: str | None = None):
        scopes[0]["symbols"].append(
            {
                "name": name,
                "kind": kind,
                "type": data_type,
                "line": 0,
                "parentClass": parent_class,
            }
        )

    def register_class(node: dict):
        name = node.get("name", "")
        extends = node.get("extends")
        if name in known_classes:
            errors.append(f"Semantic error: Class '{name}' already declared")
            return
        known_classes[name] = extends
        add_symbol(name, "class", name, parent_class=extends)
        seen: set[str] = set()
        for member in node.get("members") or []:
            if not isinstance(member, dict):
                continue
            mtype = member.get("type")
            if mtype == "VarDecl":
                mname = member.get("name", "")
                if mname in seen:
                    errors.append(f"Semantic error: Duplicate member '{mname}' in class '{name}'")
                seen.add(mname)
                add_symbol(f"{name}.{mname}", "attribute", member.get("varType", "any"), parent_class=name)
            elif mtype == "MethodDecl":
                mname = member.get("name", "")
                if mname in seen:
                    errors.append(f"Semantic error: Duplicate member '{mname}' in class '{name}'")
                seen.add(mname)
                add_symbol(
                    f"{name}.{mname}",
                    "method",
                    member.get("returnType", "void"),
                    parent_class=name,
                )

    for decl in ast.get("declarations") or []:
        if isinstance(decl, dict) and decl.get("type") == "ClassDecl":
            register_class(decl)
        elif isinstance(decl, dict) and decl.get("type") == "FuncDecl":
            add_symbol(decl.get("name", ""), "function", decl.get("returnType", "void"))

    for name, extends in known_classes.items():
        if extends and extends not in known_classes:
            errors.append(f"Semantic error: Superclass '{extends}' not found for class '{name}'")

    return ast, {"scopes": scopes}, errors
