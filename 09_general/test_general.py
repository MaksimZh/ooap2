import unittest
from typing import Any as Anything

from general import General, Any


class Boo(Any):

    def __init__(self, x: Anything, y: Anything) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def get_type(self) -> type:
        return Boo
    
class Foo(Any):

    def __init__(self, x: Anything, y: Anything) -> None:
        super().__init__()
        self.x = x
        self.y = y

    def get_type(self) -> type:
        return Foo


class Test_General(unittest.TestCase):

    def test_is_equal(self):
        f = Foo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        b = Boo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        c = Boo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        d = Boo(b.x, b.y)
        self.assertFalse(b.is_equal(f))
        self.assertFalse(b.is_equal(c))
        self.assertTrue(b.is_equal(b))
        self.assertTrue(b.is_equal(d))
        self.assertFalse(b.is_deep_equal(f))
        self.assertTrue(b.is_deep_equal(c))
        self.assertTrue(b.is_deep_equal(b))
        self.assertTrue(b.is_deep_equal(d))

    def test_copy(self):
        f = Foo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        b = Boo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        c = Boo(3, "4")
        self.assertEqual(c.get_copy_status(), General.CopyStatus.NIL)
        c.copy(f)
        self.assertEqual(c.get_copy_status(), General.CopyStatus.TYPE_MISMATCH)
        c.copy(b)
        self.assertEqual(c.get_copy_status(), General.CopyStatus.OK)
        self.assertTrue(c.is_equal(b))
        self.assertTrue(c.is_deep_equal(b))
        self.assertIs(c.x.y, b.x.y)
        self.assertIs(c.y, b.y)

    def test_deepcopy(self):
        f = Foo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        b = Boo(Boo(1, Boo(2, "3")), Boo(4, "5"))
        c = Boo(3, "4")
        self.assertEqual(c.get_deep_copy_status(), General.DeepCopyStatus.NIL)
        c.deep_copy(f)
        self.assertEqual(c.get_deep_copy_status(), General.DeepCopyStatus.TYPE_MISMATCH)
        c.deep_copy(b)
        self.assertEqual(c.get_deep_copy_status(), General.DeepCopyStatus.OK)
        self.assertFalse(c.is_equal(b))
        self.assertTrue(c.is_deep_equal(b))
        self.assertIsNot(c.x.y, b.x.y)
        self.assertIsNot(c.y, b.y)

    def test_serialize(self):
        f = Foo(Boo(1, Foo(2, "3")), Boo(4, "5"))
        self.assertEqual(
            f.serialize(),
            'Foo{x: Boo{x: int(1), y: Foo{x: int(2), y: str(3)}}, ' + \
                'y: Boo{x: int(4), y: str(5)}}')
    
    def test_deserialize(self):
        f = Foo(None, None)
        f.deserialize(
            'Foo{x: Boo{x: int(1), y: Foo{x: int(2), y: str(3)}}, ' + \
                'y: Boo{x: int(4), y: str(5)}}')
        self.assertEqual(f.get_deserialize_status(), Foo.DeserializeStatus.OK)
        self.assertTrue(f.is_deep_equal(
            Foo(Boo(1, Foo(2, "3")), Boo(4, "5"))))
        
    def test_print(self):
        f = Foo(Boo(1, Foo(2, "3")), Boo(4, "5"))
        self.assertEqual(f.print(), 'Foo(x=Boo(x=1, y=Foo(x=2, y="3")), y=Boo(x=4, y="5"))')


if __name__ == "__main__":
    unittest.main()
