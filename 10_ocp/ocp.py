from typing import Any, final
from inspect import isfunction

# ==============================================================================
# Способ 1: декоратор `@final`

class Base:

    @final
    def foo(self) -> None:
        pass


class Derived(Base):

    # Линтер будет возражать, но код выполнится без ошибок
    def foo(self) -> None:
        print("foo")


# ==============================================================================
# Способ 2: ручная проверка при создании класса (не экземпляра!)

class FinalMeta(type):
    
    def __new__(
            cls, class_name: str, bases: tuple[type, ...],
            namespace: dict[str, Any], **kwargs: Any
            ) -> type:
        # Перебираем все методы нового класса
        # и проверяем не определены ли они как `final` в классах-предках
        for name, member in namespace.items():
            if not isfunction(member):
                continue
            assert not FinalMeta.__is_final_in_base(name, bases), \
                f"Overriding final method {class_name}.{name}"
        return super().__new__(cls, class_name, bases, namespace, **kwargs)

    # Рекурсивный поиск определения метода в базовых классах
    # с проверкой не помечен ли он декоратором `final`
    @staticmethod
    def __is_final_in_base(name: str, bases: tuple[type, ...]) -> bool:
        for base in bases:
            if hasattr(base, name) and FinalMeta.__is_final(getattr(base, name)):
                return True
            if FinalMeta.__is_final_in_base(name, base.__bases__):
                return True
        return False
    
    @staticmethod
    def __is_final(func: Any) -> bool:
        return getattr(func, "__final__", False)


class FinalBase(metaclass=FinalMeta):

    @final
    def foo(self) -> None:
        pass

    def boo(self) -> None:
        pass

class FinalDerived(FinalBase):

    def boo(self) -> None:
        print("boo")

class FinalDerived2(FinalBase):

    # Линтер по-прежнему ругается
    # Но теперь получим ещё и AssertionError
    def foo(self) -> None:
        print("foo")
