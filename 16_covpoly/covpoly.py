from typing import TypeVar, Optional


class A:
    def m(self) -> str:
        return "A"

class B(A):
    def m(self) -> str:
        return "B"

class C(A):
    def m(self) -> str:
        return "C"


T = TypeVar("T", covariant=True)

class Foo:

    def polymorph(self, value: A) -> None:
        print(value.m())

    def covariant(self, values: list[T]) -> Optional[T]:
        if len(values) > 0:
            return values[0]
        else:
            return None


foo = Foo()

# Полиморфный вызов метода
a: A = B()
foo.polymorph(a)

# Ковариантный вызов метода
lb: list[B] = [B(), B()]
print(foo.covariant(lb))
