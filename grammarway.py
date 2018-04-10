class Node:
    """Doc stub"""

    def __init__(self):
        pass

    def parse(self):
        pass


class Lexeme(Node):
    """Doc stub"""

    def __init__(self):
        super().__init__()


class Empty(Lexeme):
    """Doc stub"""

    def __init__(self):
        super().__init__()


class Literal(Lexeme):
    """Doc stub"""

    def __init__(self, target):
        super().__init__()
        self.target = target
