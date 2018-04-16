from abc import ABC, abstractmethod


class Stream:
    """Doc stub"""

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    def next(self):
        self.position += 1
        return self.source[self.position - 1]


class Node(ABC):
    """Doc stub"""

    class Checker(ABC):
        """Doc stub"""

        def __init__(self, node: 'Node'):
            self.node = node
            self.status: bool = None

        @abstractmethod
        def check(self, source: str):
            raise NotImplementedError

    def __init__(self):
        self.source: str = None

    @abstractmethod
    def _parse(self, source: Stream):
        raise NotImplementedError

    def parse(self, source: str):
        self.source = Stream(source)

        self._parse(self.source)


class Lexeme(Node):
    """Doc stub"""
    pass


class Empty(Lexeme):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def check(self, source: str):
            self.status = True
            return True

    def __init__(self):
        super().__init__()

    def _parse(self, source: Stream):
        pass


class Literal(Lexeme):
    """Doc stub"""

    def __init__(self, target: str):
        super().__init__()
        self.target = target

    def _parse(self, source: Stream):
        pass
