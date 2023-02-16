from typing import Callable

class Parent:
    pass

class Child(Parent):
    pass


# Тип `Callable` - ковариантный по отношению к возвращаемому значению:

def returns_parent() -> Parent:
    return Parent()

def returns_child() -> Child:
    return Child()

# Так нельзя:
# a: Callable[[], Child] = returns_parent
# ERROR: Type "() -> Parent" cannot be assigned to type "() -> Child"
# функция может вернуть `Parent`, который не является `Child`

# А так можно:
b: Callable[[], Parent] = returns_child
# `Callable[[], Child]` - частный случай `Callable[[], Parent]`
# потому что можно подставить `Child` везде, где допустим `Parent`


# Тип `Callable` - котравариантный по отношению к аргументу:

def takes_parent(v: Parent) -> None:
    pass

def takes_child(v: Child) -> None:
    pass

# Так можно:
c: Callable[[Child], None] = takes_parent
# `Callable[[Parent], None]` - частный случай `Callable[[Child], None]`
# мы собираемся вызывать эту функцию всегда подставляя `Child`
# а `Child` можно подставить везде, где допустим `Parent`

# А так нельзя:
# d: Callable[[Parent], None] = takes_child
# ERROR: Type "(v: Child) -> None" cannot be assigned to type "(Parent) -> None"
# мы не сможем подставить ничего кроме `Child` в качестве аргумента,
# а тип функции в левой части такой, что принимает любой `Parent`