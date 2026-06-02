"""Tabela de símbolos com escopos — reuso adaptado de projeto_compiladores."""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional


class SymbolType(Enum):
    VARIABLE = "variable"
    FUNCTION = "function"
    PARAMETER = "parameter"
    CHANNEL = "channel"
    CLASS = "class"
    METHOD = "method"
    ATTRIBUTE = "attribute"


@dataclass
class Symbol:
    name: str
    symbol_type: SymbolType
    data_type: str
    scope_level: int
    line_declared: int = 0
    is_initialized: bool = True
    param_types: Optional[List[str]] = None
    return_type: Optional[str] = None
    channel_type: Optional[str] = None
    parent_class: Optional[str] = None


class Scope:
    def __init__(self, scope_level: int, scope_name: str, parent: Optional["Scope"] = None):
        self.scope_level = scope_level
        self.scope_name = scope_name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}

    def add_symbol(self, symbol: Symbol) -> bool:
        if symbol.name in self.symbols:
            return False
        self.symbols[symbol.name] = symbol
        return True

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def lookup(self, name: str) -> Optional[Symbol]:
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup(name)
        return None


class SymbolTable:
    def __init__(self):
        self.current_scope: Scope = Scope(0, "global", None)
        self.scope_stack: List[Scope] = [self.current_scope]
        self.scope_counter = 0

    def enter_scope(self, scope_name: str = "block") -> None:
        self.scope_counter += 1
        new_scope = Scope(self.scope_counter, scope_name, self.current_scope)
        self.scope_stack.append(new_scope)
        self.current_scope = new_scope

    def exit_scope(self) -> None:
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]

    def add_symbol(self, name: str, symbol_type: SymbolType, data_type: str, line: int = 0, **kwargs) -> bool:
        symbol = Symbol(
            name=name,
            symbol_type=symbol_type,
            data_type=data_type,
            scope_level=self.current_scope.scope_level,
            line_declared=line,
            **kwargs,
        )
        return self.current_scope.add_symbol(symbol)

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.current_scope.lookup(name)

    def lookup_local(self, name: str) -> Optional[Symbol]:
        return self.current_scope.lookup_local(name)

    def to_json(self) -> dict:
        scopes = []
        for scope in self.scope_stack:
            symbols = []
            for sym in scope.symbols.values():
                symbols.append(
                    {
                        "name": sym.name,
                        "kind": sym.symbol_type.value,
                        "type": sym.data_type,
                        "line": sym.line_declared,
                        "parentClass": sym.parent_class,
                    }
                )
            scopes.append({"name": scope.scope_name, "level": scope.scope_level, "symbols": symbols})
        return {"scopes": scopes}
