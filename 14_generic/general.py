from enum import Enum, auto
import pickle
import typing
from typing import final


class General:

    # КОНСТРУКТОР

    def __init__(self) -> None:
        self.__copy_status = self.CopyStatus.NIL
        self.__deep_copy_status = self.DeepCopyStatus.NIL
        self.__deserialize_status = self.DeserializeStatus.NIL
        self.__assignment_status = self.AssignmentStatus.NIL

    # Создать объект в соответствии со строковым представлением
    @final
    @classmethod
    def deserialize(cls, source: bytes) -> "General":
        try:
            obj = pickle.loads(source)
            obj.__deserialize_status = cls.DeserializeStatus.OK
            return obj
        except:
            obj = cls.__new_empty()
            obj.__deserialize_status = cls.DeserializeStatus.INVALID_SOURCE
            return obj
        
    class DeserializeStatus(Enum):
        NIL = auto(),
        OK = auto(),
        INVALID_SOURCE = auto(),
    
    __deserialize_status: DeserializeStatus

    @final
    def get_deserialize_status(self) -> DeserializeStatus:
        return self.__deserialize_status
    
    @classmethod
    def __new_empty(cls) -> "General":
        obj = cls.__new__(cls)
        General.__init__(obj)
        return obj


    # КОМАНДЫ

    # Копирование объекта `source` в данный объект
    # предусловие: тип источника совпадает с типом данного объекта
    @final
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

    @final
    def get_copy_status(self) -> CopyStatus:
        return self.__copy_status


    # Рекурсивное копирование объекта `source` в данный объект
    # предусловие: тип источника совпадает с типом данного объекта
    @final
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

    @final
    def get_deep_copy_status(self) -> DeepCopyStatus:
        return self.__deep_copy_status


    # ЗАПРОСЫ

    # Получить тип данного объекта
    @final
    def get_type(self) -> type:
        return type(self)

    # Проверить, имеет ли данный объект тип `t`
    @final
    def is_type(self, t: type) -> bool:
        return self.get_type() is t
    
    # Проверить, равен ли данный объект другому
    @final
    def is_equal(self, other: "General") -> bool:
        if other is self:
            return True
        if not other.is_type(self.get_type()):
            return False
        if vars(self).keys() != vars(other).keys():
            return False
        return self._is_content_equal(other)
    
    def _is_content_equal(self, other: "General") -> bool:
        for name, value in other.__get_contents():
            if getattr(self, name) != value:
                return False
        return True

    # Рекурсивно проверить, равен ли данный объект другому
    @final
    def is_deep_equal(self, other: "General") -> bool:
        if other is self:
            return True
        if not other.is_type(self.get_type()):
            return False
        if vars(self).keys() != vars(other).keys():
            return False
        return self._is_content_deep_equal(other)
    
    def _is_content_deep_equal(self, other: "General") -> bool:
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
    @final
    def serialize(self) -> bytes:
        return pickle.dumps(self)

    # Получить упрощённое строковое представление объекта
    @final
    def print(self) -> str:
        return _type_to_str(self.get_type()) + "(" + \
            ", ".join(name + "=" + _print(value) \
                      for name, value in self.__get_contents()) + \
            ")"

    
    # Рекурсивное создание копии данного объекта
    @final
    def clone(self) -> "General":
        other: General = self.__new_empty()
        other.deep_copy(self)
        return other
    

    # Присвоить данному объекту значение другого объекта
    @staticmethod
    def assignment_attempt(target: "General", source: "General") -> "General":
        if not issubclass(source.get_type(), target.get_type()):
            result = source.__new_empty()
            result.__assignment_status = General.AssignmentStatus.TYPE_MISMATCH
            return result
        source.__assignment_status = General.AssignmentStatus.OK
        return source

    class AssignmentStatus(Enum):
        NIL = auto(),
        OK = auto(),
        TYPE_MISMATCH = auto(),
    
    __assignment_status: AssignmentStatus

    @final
    def get_assignment_status(self) -> AssignmentStatus:
        return self.__assignment_status

    
    @final
    def __get_contents(self) -> typing.Generator[tuple[str, typing.Any], None, None]:
        for name, value in vars(self).items():
            if name.startswith("_General__"):
                continue
            yield name, value


class Any(General):
    pass

def _print(o: typing.Any) -> str:
    if isinstance(o, General):
        return o.print()
    if isinstance(o, str):
        return f'"{o}"'
    return str(o)

def _type_to_str(t: type) -> str:
    return t.__qualname__
