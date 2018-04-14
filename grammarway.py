from abc import ABC, abstractmethod

class Node:
    """Doc stub"""

    class Checker(ABC):
        """Doc stub"""

        def __init__(self, node: 'Node'):
            self.node = node

        @abstractmethod
        def check(self, source: str):
            pass


    def __init__(self):
        self.source: str = None

    def parse(self, source: str):
        self.source = source


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
