from abc import ABC, abstractmethod
from typing import TypeVar, Optional


class Stream:
    """Doc stub"""

    def __init__(self, source: str):
        self.source = source
        self.position = 0
        self.line = 1
        self.column = 1

    @property
    def next(self) -> Optional[str]:
        if self.position == len(self.source):
            return None

        self.position += 1
        return self.source[self.position - 1]


NodeType = TypeVar('NodeType', bound='Node')


class Node(ABC):
    """Doc stub"""

    class Checker(ABC):
        """Doc stub"""

        def __init__(self, node: NodeType):
            self.node = node
            self.status: bool = None

        @abstractmethod
        def check(self, source: Optional[str]):
            raise NotImplementedError

        def __call__(self, source: str):
            return self.check(source)

    CheckerType = TypeVar('CheckerType', bound=Checker)

    def __init__(self):
        self.source: str = None

    def make_checker(self) -> CheckerType:
        return self.Checker(self)

    @abstractmethod
    def _parse(self, source: Stream):
        raise NotImplementedError

    def parse(self, source: str):
        self.source = Stream(source)

        return self._parse(self.source)


class Lexeme(Node):
    """Doc stub"""

    def _parse(self, source: Stream):
        checker = self.make_checker()

        while checker.status is None:
            checker(source.next)

        return checker.status


class Empty(Lexeme):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def check(self, source: Optional[str]):
            self.status = True
            return True

    def __init__(self):
        super().__init__()


class Literal(Lexeme):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def __init__(self, node: 'Literal'):
            super().__init__(node)
            self.position: int = 0

        def check(self, source: Optional[str]):
            if source is None or source[0] != self.node.target[self.position]:
                self.status = False
                return False

            self.position += 1

            if self.position == len(self.node.target):
                self.status = True

            return True

    def __init__(self, target: str):
        super().__init__()
        self.target = target
