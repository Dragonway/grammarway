class Node:
    """Doc stub"""

    source: str = None

    def __init__(self):
        pass

    def parse(self, source: str):
        Node.source = source


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

    def __init__(self, target: str):
        super().__init__()
        self.target = target
