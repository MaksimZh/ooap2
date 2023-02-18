from abc import ABC, abstractmethod
from enum import Enum, auto

class General(ABC):

    # КОНСТРУКТОР
    def __init__(self) -> None:
        self.__copy_status = self.CopyStatus.NIL
        self.__deep_copy_status = self.DeepCopyStatus.NIL
    
    
    # КОМАНДЫ

    # Копирование объекта `source` в данный объект
    # предусловие: тип источника совпадает с типом данного объекта
    def copy(self, source: "General") -> None:
        if not source.is_type(self.get_type()):
            self.__copy_status = self.CopyStatus.TYPE_MISMATCH
            return
        for name in vars(self).keys() - vars(source).keys():
            delattr(self, name)
        for name, value in vars(source).items():
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
        for name, value in vars(source).items():
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
    

    # Рекурсивное создание копии данного объекта
    def clone(self) -> "General":
        other: General = self.__new__(self.get_type())
        other.deep_copy(self)
        return other


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
        for name, value in vars(other).items():
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
        for name, value in vars(other).items():
            this_value = getattr(self, name)
            if this_value == value:
                continue
            if not isinstance(this_value, General):
                return False
            if not this_value.is_deep_equal(value):
                return False
        return True


class Any(General):
    pass
