from abc import ABC, abstractmethod
from enum import Enum, auto
import typing


class _ID(str): pass
class _Value(str): pass
class _Open(str): pass
class _Close(str): pass
class _Error(str): pass

_Token = _ID | _Value | _Open | _Close | _Error

_Tree = tuple[str, str | list[tuple[str, "_Tree"]]]

class General(ABC):

    # КОНСТРУКТОР
    def __init__(self) -> None:
        self.__copy_status = self.CopyStatus.NIL
        self.__deep_copy_status = self.DeepCopyStatus.NIL
        self.__deserialize_status = self.DeserializeStatus.NIL
    
    
    # КОМАНДЫ

    # Копирование объекта `source` в данный объект
    # предусловие: тип источника совпадает с типом данного объекта
    def copy(self, source: "General") -> None:
        if not source.is_type(self.get_type()):
            self.__copy_status = self.CopyStatus.TYPE_MISMATCH
            return
        for name in vars(self).keys() - vars(source).keys():
            delattr(self, name)
        for name, value in source.__get_contents():
            setattr(self, name, value)
        self.__copy_status = self.CopyStatus.OK

    class CopyStatus(Enum):
        NIL = auto(),
        OK = auto(),
        TYPE_MISMATCH = auto(),
    
    __copy_status: CopyStatus

    def get_copy_status(self) -> CopyStatus:
        return self.__copy_status


    # Рекурсивное копирование объекта `source` в данный объект
    # предусловие: тип источника совпадает с типом данного объекта
    def deep_copy(self, source: "General") -> None:
        if not source.is_type(self.get_type()):
            self.__deep_copy_status = self.DeepCopyStatus.TYPE_MISMATCH
            return
        for name in vars(self).keys() - vars(source).keys():
            delattr(self, name)
        for name, value in source.__get_contents():
            new_value = value.clone() if isinstance(value, General) else value
            setattr(self, name, new_value)
        self.__deep_copy_status = self.DeepCopyStatus.OK

    class DeepCopyStatus(Enum):
        NIL = auto(),
        OK = auto(),
        TYPE_MISMATCH = auto(),
    
    __deep_copy_status: DeepCopyStatus

    def get_deep_copy_status(self) -> DeepCopyStatus:
        return self.__deep_copy_status
    
    
    # Изменить объект в соответствии со строковым представлением
    def deserialize(self, source: str) -> None:
        contents = [name for name, _ in self.__get_contents()]
        for name in contents:
            delattr(self, name)
        tokens = list[_Token]()
        _lex(source, tokens)
        if type(tokens[-1]) is _Error:
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return
        tree = _parse(tokens)
        if tree is None:
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return
        self.__deserialize_tree(tree)
        
    class DeserializeStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INVALID_SOURCE = auto(),
    
    __deserialize_status: DeserializeStatus

    def get_deserialize_status(self) -> DeserializeStatus:
        return self.__deserialize_status
    
    def __deserialize_tree(self, tree: _Tree) -> None:
        type_id, entries = tree
        self.__find_subclass(type_id)
        if type_id not in self.__subclasses:
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return
        type_ = self.__deserialize_type(type_id)
        if self.__deserialize_status != self.DeserializeStatus.OK:
            return
        if type_ is not self.get_type():
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return
        if not isinstance(entries, list):
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return
        for name, value_tree in entries:
            value_type_id = value_tree[0]
            if value_type_id in __builtins__:
                setattr(self, name, __builtins__[value_type_id](value_tree[1]))
                continue
            value_type = self.__deserialize_type(value_type_id)
            if self.__deserialize_status != self.DeserializeStatus.OK:
                return
            value = General.__new__(value_type)
            General.__init__(value)
            value.__deserialize_tree(value_tree)
            setattr(self, name, value)
        self.__deserialize_status = self.DeserializeStatus.OK

    def __deserialize_type(self, id: str) -> type:
        self.__find_subclass(id)
        if id not in self.__subclasses:
            self.__deserialize_status = self.DeserializeStatus.INVALID_SOURCE
            return General
        self.__deserialize_status = self.DeserializeStatus.OK
        return self.__subclasses[id]


    # ЗАПРОСЫ

    # Получить тип данного объекта
    @abstractmethod
    def get_type(self) -> type:
        assert False

    # Проверить, имеет ли данный объект тип `t`
    def is_type(self, t: type) -> bool:
        return self.get_type() is t
    
    # Проверить, равен ли данный объект другому
    def is_equal(self, other: "General") -> bool:
        if other is self:
            return True
        if not other.is_type(self.get_type()):
            return False
        if vars(self).keys() != vars(other).keys():
            return False
        for name, value in other.__get_contents():
            if getattr(self, name) != value:
                return False
        return True

    # Рекурсивно проверить, равен ли данный объект другому
    def is_deep_equal(self, other: "General") -> bool:
        if other is self:
            return True
        if not other.is_type(self.get_type()):
            return False
        if vars(self).keys() != vars(other).keys():
            return False
        for name, value in other.__get_contents():
            this_value = getattr(self, name)
            if this_value == value:
                continue
            if not isinstance(this_value, General):
                return False
            if not this_value.is_deep_equal(value):
                return False
        return True
    
    # Получить строковое представление объекта
    def serialize(self) -> str:
        return _type_to_str(self.get_type()) + "{" + \
            ", ".join(name + ": " + _serialize(value) \
                      for name, value in self.__get_contents()) + \
            "}"
    
    # Рекурсивное создание копии данного объекта
    def clone(self) -> "General":
        other: General = self.__new__(self.get_type())
        General.__init__(other)
        other.deep_copy(self)
        return other

    
    def __get_contents(self) -> typing.Generator[tuple[str, typing.Any], None, None]:
        for name, value in vars(self).items():
            if name.startswith("_General__"):
                continue
            yield name, value

    
    __subclasses: typing.ClassVar[dict[str, type]] = dict()

    @staticmethod
    def __register_subclasses(base: type) -> None:
        General.__subclasses[base.__qualname__] = base
        for sub in base.__subclasses__():
            General.__register_subclasses(sub)

    @staticmethod
    def __find_subclass(name: str) -> None:
        if name in General.__subclasses:
            return
        General.__register_subclasses(General)


class Any(General):
    pass

def _serialize(o: typing.Any) -> str:
    if isinstance(o, General):
        return o.serialize()
    if isinstance(o, str):
        o = o \
            .replace("{", "\\{") \
            .replace("}", "\\}") \
            .replace("(", "\\(") \
            .replace(")", "\\)") \
            .replace("\\", "\\\\")
    return _type_to_str(type(o)) + '(' + str(o) + ')'

def _lex(s: str, acc: list[_Token]) -> None:
    if len(s) == 0:
        return
    match s[0]:
        case "{" | "(" | "\\":
            acc.append(_Error(s))
            return
        case "}" | ")":
            acc.append(_Close(s[0]))
            _lex(s[1:], acc)
        case " " | "," | ":":
            _lex(s[1:], acc)
        case _:
            acc.append(_ID(""))
            _lex_id(s, acc)

def _lex_id(s: str, acc: list[_Token]) -> None:
    if len(s) == 0:
        return
    match s[0]:
        case "}" | ")" | "\\" | ",":
            acc.append(_Error(s))
            return
        case ":" | " ":
            _lex(s[1:], acc)
        case "{":
            acc.append(_Open(s[0]))
            _lex(s[1:], acc)
        case "(":
            acc.append(_Value(""))
            _lex_value(s[1:], acc)
        case _:
            acc[-1] = _ID(acc[-1] + s[0])
            _lex_id(s[1:], acc)

def _lex_value(s: str, acc: list[_Token]) -> None:
    if len(s) == 0:
        return
    match s[0]:
        case "{" | "}" | "(":
            acc.append(_Error(s))
            return
        case "\\":
            _lex_escape(s[1:], acc)
        case ")":
            _lex(s[1:], acc)
        case _:
            _lex_value_char(s, acc)

def _lex_value_char(s: str, acc: list[_Token]) -> None:
    assert len(s) > 0
    acc[-1] = _Value(acc[-1] + s[0])
    _lex_value(s[1:], acc)

def _lex_escape(s: str, acc: list[_Token]) -> None:
    if len(s) == 0:
        acc.append(_Error(""))
        return
    match s[0]:
        case "{" | "}" | "(" | ")" | "\\":
            _lex_value_char(s[1:], acc)
        case _:
            acc.append(_Error(s))

def _type_to_str(t: type) -> str:
    return t.__qualname__

def _parse(tokens: list[_Token]) -> typing.Optional[_Tree]:
    if len(tokens) < 2:
        return None
    t = tokens.pop(0)
    if type(t) is not _ID:
        return None
    type_id = str(t)
    t = tokens.pop(0)
    if type(t) is _Value:
        return type_id, str(t)
    if type(t) is not _Open:
        return None
    value = list[tuple[str, typing.Any]]()
    if len(tokens) == 0:
        return None
    t = tokens.pop(0)
    while type(t) is not _Close:
        if type(t) is not _ID:
            return None
        name = str(t)
        v = _parse(tokens)
        if v is None:
            return None
        value.append((name, v))
        if len(tokens) == 0:
            return None
        t = tokens.pop(0)
    return type_id, value
