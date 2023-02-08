from typing import Type, Generic, TypeVar
from abc import ABC

class Node(ABC):
    ...

class List(ABC):
    ...

def MakeListType(NodeType: Type[Node]) -> Type[List]:

    class MyList(List):
        __head: NodeType
        ...

    return MyList


T = TypeVar("T", bound=Node)

class List2(Generic[T]):
    __head: T
    ...


def foo(a: int | float | str) -> str:
    match a:
        case int():
            return str(a + 1)
        case float():
            return str(a + 0.1)
        case str():
            return a + "1"

print(foo(42))
print(foo(4.2))
print(foo("42"))