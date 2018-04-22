import unittest
import grammarway as gw


class TestLexemes(unittest.TestCase):

    def test_empty(self):
        empty = gw.Empty()

        self.assertTrue(empty.parse("grammarway"))
        self.assertTrue(empty.parse(" grammarway"))
        self.assertTrue(empty.parse(""))

    def test_literal(self):
        literal = gw.Literal("grammarway")

        self.assertTrue(literal.parse("grammarway"))
        self.assertTrue(literal.parse("grammarways"))
        self.assertFalse(literal.parse("grammarwei"))
        self.assertFalse(literal.parse("drammarway"))
        self.assertFalse(literal.parse("grammar"))

    def _test_and(self, node: gw.And):
        self.assertTrue(node.parse("grammarway"))
        self.assertTrue(node.parse("grammarways"))
        self.assertFalse(node.parse("grammarwei"))
        self.assertFalse(node.parse("drammarway"))
        self.assertFalse(node.parse("grammar"))

    def test_and(self):
        and1 = gw.Literal("grammar") + gw.Literal("way")
        self._test_and(and1)

        and2 = gw.Empty() + and1
        self._test_and(and2)

        and3 = and2 + gw.Empty()
        self._test_and(and3)

    def _test_or(self, node: gw.Or):
        self.assertTrue(node.parse("grammar"))
        self.assertTrue(node.parse("grammarway"))
        self.assertTrue(node.parse("way"))
        self.assertFalse(node.parse("grammaway"))

    def test_or(self):
        or1 = gw.Literal("grammar") | gw.Literal("way")
        self._test_or(or1)

        or2 = gw.Empty() | or1
        self._test_or(or2)

        or3 = or2 | gw.Empty()
        self._test_or(or3)


if __name__ == '__main__':
    unittest.main()
