from abc import ABC, abstractmethod
from typing import TypeVar, Optional, List, Union


class GrammarwayError(Exception):
    pass


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

    def step_back(self):
        if self.position == 0:
            raise GrammarwayError("'step_back' called before actual position changing")

        self.position -= 1


NodeType = TypeVar('NodeType', bound='Node')


class Node(ABC):
    """Doc stub"""

    class Checker(ABC):
        """Doc stub"""

        def __init__(self, node: NodeType):
            self.node = node
            self.status: Optional[bool] = None

        @abstractmethod
        def _check(self, source: Optional[str]) -> bool:
            raise NotImplementedError

        def check(self, source: Optional[str]) -> bool:
            if self.status is not None:
                raise GrammarwayError("Called already completed checker")

            return self._check(source)

        def __call__(self, source: str):
            return self.check(source)

    CheckerType = TypeVar('CheckerType', bound=Checker)

    def __init__(self):
        self.source: Optional[str] = None

    def make_checker(self) -> CheckerType:
        return self.Checker(self)

    @abstractmethod
    def _parse(self, source: Stream):
        raise NotImplementedError

    def parse(self, source: Union[str, Stream]):
        if isinstance(source, str):
            source = Stream(source)

        self.source = source

        return self._parse(self.source)

    def __add__(self, other: NodeType) -> 'And':
        return And(self, other)

    def __and__(self, other: NodeType) -> 'And':
        return self.__add__(other)

    def __or__(self, other: NodeType) -> 'Or':
        return Or(self, other)


class And(Node):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def __init__(self, node: 'And'):
            super().__init__(node)
            self.current_node = 0
            self.current_checker: Node.CheckerType = node.nodes[self.current_node].make_checker()

        def _check(self, source: Optional[str]) -> bool:
            result = self.current_checker(source)

            if self.current_checker.status is not None:
                if self.current_checker.status:
                    self.current_node += 1
                    if self.current_node == len(self.node.nodes):
                        self.status = True
                    else:
                        self.current_checker = self.node.nodes[self.current_node].make_checker()
                else:
                    self.status = False

            return result

    def __init__(self, node1: NodeType, node2: NodeType):
        super().__init__()
        self.nodes: List[NodeType] = [node1, node2]

    def _parse(self, source: Stream):
        return all(node.parse(source) for node in self.nodes)


class Or(Node):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def __init__(self, node: 'Or'):
            super().__init__(node)
            self.accepted_nodes: List[NodeType] = []
            self.checkers: List[Node.CheckerType] = [node.make_checker() for node in self.node.nodes]

        def _check(self, source: Optional[str]) -> bool:
            result = False
            accepted_nodes = []
            for checker in self.checkers[:]:
                if not checker(source):
                    self.checkers.remove(checker)
                else:
                    result = True
                    if checker.status is not None:
                        self.checkers.remove(checker)
                        accepted_nodes.append(checker.node)

            if accepted_nodes:
                self.accepted_nodes = accepted_nodes

            if not self.checkers:
                self.status = bool(self.accepted_nodes)

            return result

    def __init__(self, node1: NodeType, node2: NodeType):
        super().__init__()
        self.nodes: List[NodeType] = [node1, node2]

    def _parse(self, source: Stream):
        checker = self.make_checker()

        while checker.status is None:
            if not checker(source.next):
                source.step_back()

        return checker.status


class Lexeme(Node):
    """Doc stub"""

    def _parse(self, source: Stream):
        checker = self.make_checker()

        while checker.status is None:
            if not checker(source.next):
                source.step_back()

        return checker.status


class Empty(Lexeme):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def _check(self, source: Optional[str]) -> bool:
            self.status = True
            return False

    def __init__(self):
        super().__init__()


class Literal(Lexeme):
    """Doc stub"""

    class Checker(Node.Checker):
        """Doc stub"""

        def __init__(self, node: 'Literal'):
            super().__init__(node)
            self.position: int = 0

        def _check(self, source: Optional[str]) -> bool:
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
