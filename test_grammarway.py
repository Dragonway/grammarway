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


if __name__ == '__main__':
    unittest.main()
