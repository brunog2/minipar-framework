"""Parser descendente recursivo MiniPar 2026.1 — procedural + OO."""

from typing import List, Optional

from minipar_core.ast_nodes import *
from minipar_core.lexer import Token, TokenType


class Parser:
    TYPE_TOKENS = {
        TokenType.NUMBER,
        TokenType.STRING,
        TokenType.BOOL,
        TokenType.VOID,
        TokenType.LIST,
        TokenType.DICT,
        TokenType.ANY,
        TokenType.IDENTIFIER,
    }

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def current(self) -> Token:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else self.tokens[-1]

    def peek(self, offset: int = 0) -> Token:
        pos = self.pos + offset
        return self.tokens[pos] if pos < len(self.tokens) else self.tokens[-1]

    def advance(self) -> Token:
        token = self.current()
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
        return token

    def match(self, *types: TokenType) -> bool:
        return self.current().type in types

    def consume(self, token_type: TokenType, msg: str | None = None) -> Token:
        if not self.match(token_type):
            msg = msg or f"Expected {token_type.name}"
            self.error(msg)
        return self.advance()

    def error(self, msg: str):
        token = self.current()
        raise SyntaxError(f"Parser error at {token.line}:{token.column}: {msg}")

    def parse(self) -> Program:
        declarations = []
        while not self.match(TokenType.EOF):
            declarations.append(self.declaration())
        return Program(declarations=declarations)

    def is_type_token(self, tt: TokenType) -> bool:
        return tt in self.TYPE_TOKENS

    def is_oo_var_start(self) -> bool:
        if self.match(TokenType.EOF):
            return False
        if not self.is_type_token(self.current().type):
            return False
        if self.peek(1).type != TokenType.IDENTIFIER:
            return False
        if self.peek(2).type in (TokenType.ASSIGN, TokenType.SEMICOLON):
            return True
        return False

    def is_method_start(self) -> bool:
        if not self.is_type_token(self.current().type):
            return False
        if self.peek(1).type != TokenType.IDENTIFIER:
            return False
        return self.peek(2).type == TokenType.LPAREN

    def is_constructor_start(self, class_name: str) -> bool:
        return (
            self.match(TokenType.IDENTIFIER)
            and self.current().value == class_name
            and self.peek(1).type == TokenType.LPAREN
        )

    def declaration(self) -> ASTNode:
        if self.match(TokenType.CLASS):
            return self.class_declaration()
        if self.match(TokenType.FUNC):
            return self.func_declaration()
        if self.match(TokenType.VAR):
            return self.var_declaration()
        if self.match(TokenType.S_CHANNEL, TokenType.C_CHANNEL):
            return self.channel_declaration()
        if self.match(TokenType.SEQ):
            return self.seq_block()
        if self.match(TokenType.PAR):
            return self.par_block()
        if self.is_oo_var_start():
            return self.oo_var_declaration()
        return self.statement()

    def class_declaration(self) -> ClassDecl:
        self.consume(TokenType.CLASS)
        name = self.consume(TokenType.IDENTIFIER, "Expected class name").value
        extends = None
        if self.match(TokenType.EXTENDS):
            self.advance()
            extends = self.consume(TokenType.IDENTIFIER, "Expected superclass name").value
        self.consume(TokenType.LBRACE)
        members: List[ASTNode] = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            if self.is_oo_var_start():
                members.append(self.oo_var_declaration())
            elif self.is_constructor_start(name):
                members.append(self.constructor_declaration(name))
            elif self.is_method_start():
                members.append(self.method_declaration())
            else:
                self.error("Expected attribute, constructor or method in class body")
        self.consume(TokenType.RBRACE)
        return ClassDecl(name=name, extends=extends, members=members)

    def oo_var_declaration(self) -> VarDecl:
        var_type = self.type_specifier()
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.expression()
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return VarDecl(var_type=var_type, name=name, initializer=initializer)

    def method_declaration(self) -> MethodDecl:
        return_type = self.type_specifier()
        name = self.consume(TokenType.IDENTIFIER, "Expected method name").value
        self.consume(TokenType.LPAREN)
        parameters = self.oo_parameters()
        self.consume(TokenType.RPAREN)
        body = self.block()
        return MethodDecl(return_type=return_type, name=name, parameters=parameters, body=body)

    def constructor_declaration(self, class_name: str) -> MethodDecl:
        self.advance()  # class name token
        self.consume(TokenType.LPAREN)
        parameters = self.oo_parameters()
        self.consume(TokenType.RPAREN)
        body = self.block()
        return MethodDecl(
            return_type=class_name,
            name=class_name,
            parameters=parameters,
            body=body,
            is_constructor=True,
        )

    def oo_parameters(self) -> List[Parameter]:
        params: List[Parameter] = []
        if not self.match(TokenType.RPAREN):
            params.append(self.oo_parameter())
            while self.match(TokenType.COMMA):
                self.advance()
                params.append(self.oo_parameter())
        return params

    def oo_parameter(self) -> Parameter:
        param_type = self.type_specifier()
        name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
        return Parameter(name=name, param_type=param_type)

    def func_declaration(self) -> FuncDecl:
        self.consume(TokenType.FUNC)
        name = self.consume(TokenType.IDENTIFIER, "Expected function name").value
        self.consume(TokenType.LPAREN)
        parameters = []
        if not self.match(TokenType.RPAREN):
            parameters.append(self.parameter())
            while self.match(TokenType.COMMA):
                self.advance()
                parameters.append(self.parameter())
        self.consume(TokenType.RPAREN)
        self.consume(TokenType.ARROW, "Expected '->' after parameter list")
        return_type = self.type_specifier()
        body = self.block()
        return FuncDecl(return_type=return_type, name=name, parameters=parameters, body=body)

    def parameter(self) -> VarDecl:
        name = self.consume(TokenType.IDENTIFIER, "Expected parameter name").value
        self.consume(TokenType.COLON, "Expected ':' after parameter name")
        param_type = self.type_specifier()
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.expression()
        return VarDecl(var_type=param_type, name=name, initializer=initializer)

    def var_declaration(self) -> VarDecl:
        self.consume(TokenType.VAR)
        name = self.consume(TokenType.IDENTIFIER, "Expected variable name").value
        self.consume(TokenType.COLON)
        var_type = self.type_specifier()
        initializer = None
        if self.match(TokenType.ASSIGN):
            self.advance()
            initializer = self.expression()
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return VarDecl(var_type=var_type, name=name, initializer=initializer)

    def channel_declaration(self) -> ChannelDecl:
        channel_type = "s_channel" if self.match(TokenType.S_CHANNEL) else "c_channel"
        self.advance()
        name = self.consume(TokenType.IDENTIFIER).value
        # Accept both `{}` and `()` as argument delimiters
        if self.match(TokenType.LBRACE):
            self.advance()
            arguments = []
            if not self.match(TokenType.RBRACE):
                arguments.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.expression())
            self.consume(TokenType.RBRACE)
        elif self.match(TokenType.LPAREN):
            self.advance()
            arguments = []
            if not self.match(TokenType.RPAREN):
                arguments.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    arguments.append(self.expression())
            self.consume(TokenType.RPAREN)
        else:
            arguments = []
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return ChannelDecl(channel_type=channel_type, name=name, arguments=arguments)

    def send_statement(self) -> SendStmt:
        self.consume(TokenType.SEND)
        self.consume(TokenType.LPAREN)
        channel = self.consume(TokenType.IDENTIFIER, "Expected channel name").value
        self.consume(TokenType.COMMA)
        value = self.expression()
        self.consume(TokenType.RPAREN)
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return SendStmt(channel=channel, value=value)

    def receive_statement(self) -> ReceiveStmt:
        self.consume(TokenType.RECEIVE)
        self.consume(TokenType.LPAREN)
        channel = self.consume(TokenType.IDENTIFIER, "Expected channel name").value
        self.consume(TokenType.COMMA)
        target = self.consume(TokenType.IDENTIFIER, "Expected target variable").value
        self.consume(TokenType.RPAREN)
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return ReceiveStmt(channel=channel, target=target)

    def type_specifier(self) -> str:
        if self.match(TokenType.NUMBER):
            self.advance()
            return "number"
        if self.match(TokenType.STRING):
            self.advance()
            return "string"
        if self.match(TokenType.BOOL):
            self.advance()
            return "bool"
        if self.match(TokenType.VOID):
            self.advance()
            return "void"
        if self.match(TokenType.LIST):
            self.advance()
            return "list"
        if self.match(TokenType.DICT):
            self.advance()
            return "dict"
        if self.match(TokenType.ANY):
            self.advance()
            return "any"
        if self.match(TokenType.IDENTIFIER):
            return self.advance().value
        self.error("Expected type specifier")

    def block(self) -> Block:
        self.consume(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            statements.append(self.statement())
        self.consume(TokenType.RBRACE)
        return Block(statements=statements)

    def statement(self) -> ASTNode:
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.SEQ):
            return self.seq_block()
        if self.match(TokenType.PAR):
            return self.par_block()
        if self.match(TokenType.RETURN):
            return self.return_statement()
        if self.match(TokenType.BREAK):
            return self.break_statement()
        if self.match(TokenType.CONTINUE):
            return self.continue_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement(newline=False)
        if self.match(TokenType.PRINTLN):
            return self.print_statement(newline=True)
        if self.match(TokenType.SEND):
            return self.send_statement()
        if self.match(TokenType.RECEIVE):
            return self.receive_statement()
        if self.match(TokenType.S_CHANNEL, TokenType.C_CHANNEL):
            return self.channel_declaration()
        if self.match(TokenType.LBRACE):
            return self.block()
        if self.match(TokenType.VAR):
            return self.var_declaration()
        if self.match(TokenType.FUNC):
            return self.func_declaration()
        if self.is_oo_var_start():
            return self.oo_var_declaration()
        return self.expression_statement()

    def print_statement(self, newline: bool) -> PrintStmt:
        self.advance()
        self.consume(TokenType.LPAREN)
        arguments = []
        if not self.match(TokenType.RPAREN):
            arguments.append(self.expression())
            while self.match(TokenType.COMMA):
                self.advance()
                arguments.append(self.expression())
        self.consume(TokenType.RPAREN)
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return PrintStmt(arguments=arguments, newline=newline)

    def if_statement(self) -> IfStmt:
        self.consume(TokenType.IF)
        self.consume(TokenType.LPAREN)
        condition = self.expression()
        self.consume(TokenType.RPAREN)
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            self.advance()
            else_branch = self.statement()
        return IfStmt(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def while_statement(self) -> WhileStmt:
        self.consume(TokenType.WHILE)
        self.consume(TokenType.LPAREN)
        condition = self.expression()
        self.consume(TokenType.RPAREN)
        body = self.statement()
        return WhileStmt(condition=condition, body=body)

    def for_statement(self) -> ForStmt:
        self.consume(TokenType.FOR)
        self.consume(TokenType.LPAREN)
        self.consume(TokenType.VAR)
        var_name = self.consume(TokenType.IDENTIFIER).value
        self.consume(TokenType.COLON)
        var_type = self.type_specifier()
        variable = VarDecl(var_type=var_type, name=var_name)
        self.consume(TokenType.IN)
        iterable = self.expression()
        self.consume(TokenType.RPAREN)
        body = self.statement()
        return ForStmt(variable=variable, iterable=iterable, body=body)

    def return_statement(self) -> ReturnStmt:
        self.consume(TokenType.RETURN)
        value = None
        if not self.match(TokenType.SEMICOLON) and not self.match(TokenType.RBRACE):
            value = self.expression()
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return ReturnStmt(value=value)

    def break_statement(self) -> BreakStmt:
        self.consume(TokenType.BREAK)
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return BreakStmt()

    def continue_statement(self) -> ContinueStmt:
        self.consume(TokenType.CONTINUE)
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return ContinueStmt()

    def seq_block(self) -> SeqBlock:
        self.consume(TokenType.SEQ)
        self.consume(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            statements.append(self.statement())
        self.consume(TokenType.RBRACE)
        return SeqBlock(statements=statements)

    def par_block(self) -> ParBlock:
        self.consume(TokenType.PAR)
        self.consume(TokenType.LBRACE)
        statements = []
        while not self.match(TokenType.RBRACE) and not self.match(TokenType.EOF):
            statements.append(self.statement())
        self.consume(TokenType.RBRACE)
        return ParBlock(statements=statements)

    def expression_statement(self) -> ExprStmt:
        expr = self.expression()
        if self.match(TokenType.SEMICOLON):
            self.advance()
        return ExprStmt(expression=expr)

    def expression(self) -> ASTNode:
        return self.assignment()

    def assignment(self) -> ASTNode:
        expr = self.logical_or()
        if self.match(TokenType.ASSIGN):
            self.advance()
            value = self.assignment()
            if isinstance(expr, Variable):
                return Assignment(name=expr.name, value=value)
            if isinstance(expr, PropertyAccess):
                return PropertyAssign(
                    receiver=expr.receiver,
                    property_name=expr.property_name,
                    value=value,
                )
            self.error("Invalid assignment target")
        return expr

    def logical_or(self) -> ASTNode:
        expr = self.logical_and()
        while self.match(TokenType.OR):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.logical_and())
        return expr

    def logical_and(self) -> ASTNode:
        expr = self.equality()
        while self.match(TokenType.AND):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.equality())
        return expr

    def equality(self) -> ASTNode:
        expr = self.comparison()
        while self.match(TokenType.EQ, TokenType.NEQ):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.comparison())
        return expr

    def comparison(self) -> ASTNode:
        expr = self.term()
        while self.match(TokenType.LT, TokenType.GT, TokenType.LTE, TokenType.GTE):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.term())
        return expr

    def term(self) -> ASTNode:
        expr = self.factor()
        while self.match(TokenType.PLUS, TokenType.MINUS):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.factor())
        return expr

    def factor(self) -> ASTNode:
        expr = self.unary()
        while self.match(TokenType.MULTIPLY, TokenType.DIVIDE, TokenType.MODULO):
            op = self.advance().value
            expr = BinaryOp(left=expr, operator=op, right=self.unary())
        return expr

    def unary(self) -> ASTNode:
        if self.match(TokenType.NOT, TokenType.MINUS):
            op = self.advance().value
            return UnaryOp(operator=op, operand=self.unary())
        return self.call()

    def call(self) -> ASTNode:
        expr = self.primary()
        while True:
            if self.match(TokenType.DOT):
                self.advance()
                prop = self.consume(TokenType.IDENTIFIER, "Expected property or method name").value
                if self.match(TokenType.LPAREN):
                    self.advance()
                    args = []
                    if not self.match(TokenType.RPAREN):
                        args.append(self.expression())
                        while self.match(TokenType.COMMA):
                            self.advance()
                            args.append(self.expression())
                    self.consume(TokenType.RPAREN)
                    expr = MethodCall(receiver=expr, method=prop, arguments=args)
                else:
                    expr = PropertyAccess(receiver=expr, property_name=prop)
            elif self.match(TokenType.LBRACKET):
                self.advance()
                if self.match(TokenType.COLON):
                    self.advance()
                    end = None if self.match(TokenType.RBRACKET) else self.expression()
                    self.consume(TokenType.RBRACKET)
                    expr = SliceAccess(object=expr, start=None, end=end)
                else:
                    first = self.expression()
                    if self.match(TokenType.COLON):
                        self.advance()
                        end = None if self.match(TokenType.RBRACKET) else self.expression()
                        self.consume(TokenType.RBRACKET)
                        expr = SliceAccess(object=expr, start=first, end=end)
                    else:
                        self.consume(TokenType.RBRACKET)
                        expr = IndexAccess(object=expr, index=first)
            elif self.match(TokenType.LPAREN):
                self.advance()
                args = []
                if not self.match(TokenType.RPAREN):
                    args.append(self.expression())
                    while self.match(TokenType.COMMA):
                        self.advance()
                        args.append(self.expression())
                self.consume(TokenType.RPAREN)
                if isinstance(expr, Variable):
                    expr = FuncCall(name=expr.name, arguments=args)
                else:
                    self.error("Invalid function call")
            else:
                break
        return expr

    def primary(self) -> ASTNode:
        if self.match(TokenType.TRUE):
            self.advance()
            return BoolLiteral(value=True)
        if self.match(TokenType.FALSE):
            self.advance()
            return BoolLiteral(value=False)
        if self.match(TokenType.NUMBER_LITERAL):
            return NumberLiteral(value=self.advance().value)
        if self.match(TokenType.STRING_LITERAL):
            return StringLiteral(value=self.advance().value)
        if self.match(TokenType.THIS):
            self.advance()
            return ThisExpr()
        if self.match(TokenType.SUPER):
            self.advance()
            self.consume(TokenType.LPAREN)
            args = []
            if not self.match(TokenType.RPAREN):
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    args.append(self.expression())
            self.consume(TokenType.RPAREN)
            return SuperCall(arguments=args)
        if self.match(TokenType.NEW):
            self.advance()
            class_name = self.consume(TokenType.IDENTIFIER, "Expected class name after new").value
            self.consume(TokenType.LPAREN)
            args = []
            if not self.match(TokenType.RPAREN):
                args.append(self.expression())
                while self.match(TokenType.COMMA):
                    self.advance()
                    args.append(self.expression())
            self.consume(TokenType.RPAREN)
            return NewInstance(class_name=class_name, arguments=args)
        if self.match(TokenType.IDENTIFIER):
            return Variable(name=self.advance().value)
        if self.match(TokenType.LPAREN):
            self.advance()
            expr = self.expression()
            self.consume(TokenType.RPAREN)
            return expr
        if self.match(TokenType.LBRACKET):
            return self.list_literal()
        if self.match(TokenType.LBRACE):
            return self.dict_literal()
        self.error(f"Unexpected token: {self.current().type.name}")

    def list_literal(self) -> ListLiteral:
        self.consume(TokenType.LBRACKET)
        if self.match(TokenType.FOR):
            self.advance()
            self.consume(TokenType.LPAREN)
            self.consume(TokenType.VAR)
            var_name = self.consume(TokenType.IDENTIFIER).value
            self.consume(TokenType.COLON)
            var_type = self.type_specifier()
            variable = VarDecl(var_type=var_type, name=var_name)
            self.consume(TokenType.IN)
            iterable = self.expression()
            self.consume(TokenType.RPAREN)
            self.consume(TokenType.ARROW)
            expression = self.expression()
            self.consume(TokenType.RBRACKET)
            return ListComprehension(variable=variable, iterable=iterable, expression=expression)
        elements = []
        if not self.match(TokenType.RBRACKET):
            elements.append(self.expression())
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACKET):
                    break
                elements.append(self.expression())
        self.consume(TokenType.RBRACKET)
        return ListLiteral(elements=elements)

    def dict_literal(self) -> DictLiteral:
        self.consume(TokenType.LBRACE)
        pairs = []
        if not self.match(TokenType.RBRACE):
            key = self.expression()
            self.consume(TokenType.COLON)
            value = self.expression()
            pairs.append((key, value))
            while self.match(TokenType.COMMA):
                self.advance()
                if self.match(TokenType.RBRACE):
                    break
                key = self.expression()
                self.consume(TokenType.COLON)
                value = self.expression()
                pairs.append((key, value))
        self.consume(TokenType.RBRACE)
        return DictLiteral(pairs=pairs)
