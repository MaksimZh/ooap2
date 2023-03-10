# Динамическое связывание

В моём коде и в примерах для динамического связывание используется
перегрузка методов в классах-потомках.

В Python можно было бы использовать duck-typing,
т.е. вызывать метода объекта по имени в надежде, что он определён.
Лично мне такой подход не нравится, потому что тут слишком много свободы,
неопределённости и пространства для ошибок.

При использовании наследования линтер может проверить типы и помочь найти
ошибки на этапе написания кода.
Если же мы имеем дело, например, с чужим кодом,
где нельзя добавить наследование, то можно использовать протоколы:
```Python
from typing import Protocol

class Foo(Protocol):

    def foo(self) -> None:
        pass

class A: # А не наследует Foo !!!

    def foo(self) -> None:
        pass

class B:
    pass

def func(v: Foo) -> None:
    v.foo()

func(A()) # OK
func(B()) # "B" is incompatible with protocol "Foo"
```
