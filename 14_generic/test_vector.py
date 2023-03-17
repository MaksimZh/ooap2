import unittest
from typing import Optional

from vector import HasAdd, Vector


class Int(HasAdd):

    __value: int

    def __init__(self, value: int) -> None:
        super().__init__()
        self.__value = value

    def add(self, other: HasAdd) -> "Optional[Int]":
        if other.get_type() is not Int:
            return None
        assert isinstance(other, Int)
        return Int(self.__value + other.__value)


class Test_Vector(unittest.TestCase):

    def test(self):
        a = Vector[Int](Int(1), Int(2), Int(3))
        b = Vector[Int](Int(10), Int(20), Int(30))
        c = a.add(b)
        assert c
        self.assertTrue(c.is_deep_equal(Vector[Int](Int(11), Int(22), Int(33))))

    def test_fail(self):
        a = Vector[Int](Int(1), Int(2), Int(3))
        b = Vector[Int](Int(10), Int(20))
        c = a.add(b)
        self.assertIsNone(c)

    def test_nested(self):
        a = Vector[Vector[Int]](
            Vector[Int](Int(11), Int(12), Int(13)),
            Vector[Int](Int(21), Int(22), Int(23)))
        b = Vector[Vector[Int]](
            Vector[Int](Int(1100), Int(1200), Int(1300)),
            Vector[Int](Int(2100), Int(2200), Int(2300)))
        c = a.add(b)
        assert c
        self.assertTrue(c.is_deep_equal(Vector[Vector[Int]](
            Vector[Int](Int(1111), Int(1212), Int(1313)),
            Vector[Int](Int(2121), Int(2222), Int(2323)))))

    def test_nested_2(self):
        a = Vector[Vector[Vector[Int]]](
            Vector[Vector[Int]](
                Vector[Int](Int(111), Int(112), Int(113)),
                Vector[Int](Int(121), Int(122), Int(123))),
            Vector[Vector[Int]](
                Vector[Int](Int(211), Int(212), Int(213)),
                Vector[Int](Int(221), Int(222), Int(223))))
        b = Vector[Vector[Vector[Int]]](
            Vector[Vector[Int]](
                Vector[Int](Int(111000), Int(112000), Int(113000)),
                Vector[Int](Int(121000), Int(122000), Int(123000))),
            Vector[Vector[Int]](
                Vector[Int](Int(211000), Int(212000), Int(213000)),
                Vector[Int](Int(221000), Int(222000), Int(223000))))
        c = a.add(b)
        assert c
        self.assertTrue(c.is_deep_equal(Vector[Vector[Vector[Int]]](
            Vector[Vector[Int]](
                Vector[Int](Int(111111), Int(112112), Int(113113)),
                Vector[Int](Int(121121), Int(122122), Int(123123))),
            Vector[Vector[Int]](
                Vector[Int](Int(211211), Int(212212), Int(213213)),
                Vector[Int](Int(221221), Int(222222), Int(223223))))))


if __name__ == "__main__":
    unittest.main()
