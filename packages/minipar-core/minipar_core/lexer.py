"""Lexer MiniPar 2026.1 — base projeto_compiladores + tokens OO (cl-minipar)."""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional


class TokenType(Enum):
    BREAK = auto()
    C_CHANNEL = auto()
    CLASS = auto()
    CONTINUE = auto()
    DO = auto()
    ELSE = auto()
    EXTENDS = auto()
    FALSE = auto()
    FOR = auto()
    FUNC = auto()
    IF = auto()
    IN = auto()
    INPUT = auto()
    NEW = auto()
    PAR = auto()
    PRINT = auto()
    PRINTLN = auto()
    RETURN = auto()
    S_CHANNEL = auto()
    SEQ = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()
    NUMBER = auto()
    STRING = auto()
    BOOL = auto()
    VOID = auto()
    LIST = auto()
    DICT = auto()
    ANY = auto()
    NUMBER_LITERAL = auto()
    STRING_LITERAL = auto()
    IDENTIFIER = auto()
    PLUS = auto()
    MINUS = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    MODULO = auto()
    NOT = auto()
    EQ = auto()
    NEQ = auto()
    LTE = auto()
    GTE = auto()
    LT = auto()
    GT = auto()
    ASSIGN = auto()
    AND = auto()
    OR = auto()
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    ARROW = auto()
    DOT = auto()
    EOF = auto()


@dataclass
class Token:
    type: TokenType
    value: object
    line: int
    column: int


class Lexer:
    KEYWORDS = {
        "break": TokenType.BREAK,
        "c_channel": TokenType.C_CHANNEL,
        "class": TokenType.CLASS,
        "continue": TokenType.CONTINUE,
        "do": TokenType.DO,
        "else": TokenType.ELSE,
        "extends": TokenType.EXTENDS,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "func": TokenType.FUNC,
        "if": TokenType.IF,
        "in": TokenType.IN,
        "input": TokenType.INPUT,
        "new": TokenType.NEW,
        "par": TokenType.PAR,
        "print": TokenType.PRINT,
        "println": TokenType.PRINTLN,
        "return": TokenType.RETURN,
        "s_channel": TokenType.S_CHANNEL,
        "seq": TokenType.SEQ,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
        "number": TokenType.NUMBER,
        "string": TokenType.STRING,
        "bool": TokenType.BOOL,
        "void": TokenType.VOID,
        "list": TokenType.LIST,
        "dict": TokenType.DICT,
        "any": TokenType.ANY,
    }

    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: List[Token] = []

    def error(self, msg: str):
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {msg}")

    def peek(self, offset: int = 0) -> Optional[str]:
        pos = self.pos + offset
        return self.source[pos] if pos < len(self.source) else None

    def advance(self) -> Optional[str]:
        if self.pos >= len(self.source):
            return None
        char = self.source[self.pos]
        self.pos += 1
        if char == "\n":
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return char

    def skip_whitespace(self):
        while self.peek() and self.peek() in " \t\r\n":
            self.advance()

    def skip_comment(self):
        if self.peek() == "#":
            while self.peek() and self.peek() != "\n":
                self.advance()
            return True
        if self.peek() == "/" and self.peek(1) == "*":
            self.advance()
            self.advance()
            while self.peek():
                if self.peek() == "*" and self.peek(1) == "/":
                    self.advance()
                    self.advance()
                    return True
                self.advance()
            self.error("Unterminated multi-line comment")
        return False

    def read_number(self) -> Token:
        start_line, start_col = self.line, self.column
        num_str = ""
        has_dot = False
        while self.peek() and (self.peek().isdigit() or self.peek() == "."):
            if self.peek() == ".":
                if has_dot:
                    break
                has_dot = True
            num_str += self.advance()
        value = float(num_str) if has_dot else int(num_str)
        return Token(TokenType.NUMBER_LITERAL, value, start_line, start_col)

    def read_string(self) -> Token:
        start_line, start_col = self.line, self.column
        self.advance()
        string_val = ""
        while self.peek() and self.peek() != '"':
            if self.peek() == "\\":
                self.advance()
                next_char = self.advance()
                escapes = {"n": "\n", "t": "\t", '"': '"', "\\": "\\"}
                string_val += escapes.get(next_char, next_char or "")
            else:
                string_val += self.advance()
        if not self.peek():
            self.error("Unterminated string literal")
        self.advance()
        return Token(TokenType.STRING_LITERAL, string_val, start_line, start_col)

    def read_identifier(self) -> Token:
        start_line, start_col = self.line, self.column
        ident = ""
        while self.peek() and (self.peek().isalnum() or self.peek() == "_"):
            ident += self.advance()
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, start_line, start_col)

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.source):
            self.skip_whitespace()
            if self.pos >= len(self.source):
                break
            if self.skip_comment():
                continue

            start_line, start_col = self.line, self.column
            char = self.peek()

            if char.isdigit():
                self.tokens.append(self.read_number())
            elif char == '"':
                self.tokens.append(self.read_string())
            elif char.isalpha() or char == "_":
                self.tokens.append(self.read_identifier())
            elif char == "=" and self.peek(1) == "=":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.EQ, "==", start_line, start_col))
            elif char == "!" and self.peek(1) == "=":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.NEQ, "!=", start_line, start_col))
            elif char == "<" and self.peek(1) == "=":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.LTE, "<=", start_line, start_col))
            elif char == ">" and self.peek(1) == "=":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.GTE, ">=", start_line, start_col))
            elif char == "&" and self.peek(1) == "&":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.AND, "&&", start_line, start_col))
            elif char == "|" and self.peek(1) == "|":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.OR, "||", start_line, start_col))
            elif char == "-" and self.peek(1) == ">":
                self.advance()
                self.advance()
                self.tokens.append(Token(TokenType.ARROW, "->", start_line, start_col))
            elif char == "+":
                self.advance()
                self.tokens.append(Token(TokenType.PLUS, "+", start_line, start_col))
            elif char == "-":
                self.advance()
                self.tokens.append(Token(TokenType.MINUS, "-", start_line, start_col))
            elif char == "*":
                self.advance()
                self.tokens.append(Token(TokenType.MULTIPLY, "*", start_line, start_col))
            elif char == "/":
                self.advance()
                self.tokens.append(Token(TokenType.DIVIDE, "/", start_line, start_col))
            elif char == "%":
                self.advance()
                self.tokens.append(Token(TokenType.MODULO, "%", start_line, start_col))
            elif char == "!":
                self.advance()
                self.tokens.append(Token(TokenType.NOT, "!", start_line, start_col))
            elif char == "<":
                self.advance()
                self.tokens.append(Token(TokenType.LT, "<", start_line, start_col))
            elif char == ">":
                self.advance()
                self.tokens.append(Token(TokenType.GT, ">", start_line, start_col))
            elif char == "=":
                self.advance()
                self.tokens.append(Token(TokenType.ASSIGN, "=", start_line, start_col))
            elif char == "(":
                self.advance()
                self.tokens.append(Token(TokenType.LPAREN, "(", start_line, start_col))
            elif char == ")":
                self.advance()
                self.tokens.append(Token(TokenType.RPAREN, ")", start_line, start_col))
            elif char == "{":
                self.advance()
                self.tokens.append(Token(TokenType.LBRACE, "{", start_line, start_col))
            elif char == "}":
                self.advance()
                self.tokens.append(Token(TokenType.RBRACE, "}", start_line, start_col))
            elif char == ",":
                self.advance()
                self.tokens.append(Token(TokenType.COMMA, ",", start_line, start_col))
            elif char == ";":
                self.advance()
                self.tokens.append(Token(TokenType.SEMICOLON, ";", start_line, start_col))
            elif char == ":":
                self.advance()
                self.tokens.append(Token(TokenType.COLON, ":", start_line, start_col))
            elif char == ".":
                self.advance()
                self.tokens.append(Token(TokenType.DOT, ".", start_line, start_col))
            elif char == "[":
                self.advance()
                self.tokens.append(Token(TokenType.LBRACKET, "[", start_line, start_col))
            elif char == "]":
                self.advance()
                self.tokens.append(Token(TokenType.RBRACKET, "]", start_line, start_col))
            else:
                self.error(f"Unexpected character: '{char}'")

        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
