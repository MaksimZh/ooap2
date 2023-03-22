# Льготное наследование
# стандартный класс `str` содержит всё, что нам надо
# подклассы нужны, чтобы отличать лексические единицы друг от друга

class Token(str):
    pass

class Open(Token):
    pass

class Close(Token):
    pass

class Value(Token):
    pass

class Operator(Token):
    pass


# Наследование реализации

class Lexer:
    ...

    def is_token_ready(self) -> bool:
        ...

    def get_token(self) -> Token:
        ...

    # Возвращает новый лексический анализатор,
    # с учётом следующего символа
    def get_next(self, char: str) -> "Lexer":
        ...


# классы потомки наследуют общую реализацию
# но определяют свой метод обработки очередного символа
# каждый из них отвечает за одно из состояний лексического анализатора

class ExpressionLexer(Lexer):
    ...
    
    def get_next(self, char: str) -> "Lexer":
        ...

class ValueLexer(Lexer):
    ...
    
    def get_next(self, char: str) -> "Lexer":
        ...

class OperatorLexer(Lexer):
    ...

    def get_next(self, char: str) -> "Lexer":
        ...
