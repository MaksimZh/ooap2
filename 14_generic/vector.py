from typing import Generic, TypeVar, Optional
from general import General
from abc import ABC, abstractmethod


class HasAdd(General, ABC):
    
    @abstractmethod
    def add(self, other: "HasAdd") -> "Optional[HasAdd]":
        assert False

T = TypeVar("T", bound=HasAdd)

class Vector(HasAdd, Generic[T]):

    __data: list[General]
    
    # КОНСТРУКТОР
    def __init__(self, *args: General) -> None:
        super().__init__()
        self.__data = list(args)


    # ЗАПРОСЫ

    # Получить длину массива
    def get_size(self) -> int:
        return len(self.__data)

    # Поэлементное сложение двух массивов
    def add(self, other: HasAdd) -> "Optional[Vector[T]]":
        if not isinstance(other, Vector):
            return None
        if self.get_size() != other.get_size():
            return None
        return Vector[T](*map(lambda x, y: x.add(y), self.__data, other.__data)) #type: ignore

    # Правильное сравнение нужно для тестирования
    def _is_content_deep_equal(self, other: "General") -> bool:
        assert isinstance(other, Vector)
        if self.get_size() != other.get_size():
            return False
        for i in range(self.get_size()):
            if not self.__data[i].is_deep_equal(other.__data[i]):
                return False
        return True
