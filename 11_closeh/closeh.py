from typing import final
from general import Any

class Hello(Any):
    def hello(self) -> None:
        assert False

class Foo(Hello):
    
    # Зря я сделал `General.get_type` абстрактным. Можно же было `type(self)`...
    def get_type(self) -> type:
        return Foo
    
    def hello(self) -> None:
        print("Foo: hello")

class Boo(Hello):

    def get_type(self) -> type:
        return Boo

    def hello(self) -> None:
        print("Boo: hello")

class Bar(Hello):

    def get_type(self) -> type:
        return Bar

    def hello(self) -> None:
        print("Bar: hello")

@final
class None_(Foo, Boo, Bar):

    def get_type(self) -> type:
        return None_
    
    def hello(self) -> None:
        assert False

Void = None_()

def say(obj: Hello) -> None:
    if obj.is_equal(Void):
        print("Bye")
        return
    obj.hello()

say(Foo())  # Foo: hello
say(Boo())  # Boo: hello
say(Bar())  # Bar: hello
say(Void)   # Bye
