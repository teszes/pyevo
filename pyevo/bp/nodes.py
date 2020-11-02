class Node:

    @property
    def children(self):
        return tuple()

    @children.setter
    def children(self, value):
        raise AttributeError("Non functional node can not have children")

    @property
    def family(self) -> tuple:
        family = (self,)
        for child in self.children:
            family += child.family
        return family

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        for child in self.children:
            child.level = level + 1

    def __init__(self):
        self.parent = None
        self._level = 1
        raise ValueError("The Node base class should not be instantiated")

    def __call__(self):
        raise ValueError("Instances of the Node base class should not be called")


class Task():
    pass


class FunctionalNode(Node):
    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = tuple(children)
        for child in self._children:
            child.level = self.level + 1
            child.parent = self

    def add_child(self, child: Node):
        child.level = self.level + 1
        child.parent = self
        self._children += (child,)

    def __init__(self):
        try:
            super().__init__()
        except ValueError as exc:
            if str(exc) != "The Node base class should not be instantiated":
                raise

        self._children = tuple()

    def __call__(self):
        try:
            super().__call__()
        except ValueError as exc:
            if str(exc) != "Instances of the Node base class should not be called":
                raise


class TerminalNode(Node):
    def __init__(self):
        try:
            super().__init__()
        except ValueError as exc:
            if str(exc) != "The Node base class should not be instantiated":
                raise

    def __call__(self):
        try:
            super().__call__()
        except ValueError as exc:
            if str(exc) != "Instances of the Node base class should not be called":
                raise
