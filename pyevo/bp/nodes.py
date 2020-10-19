class Node:

    def __init__(self):
        self.level = 1


class FunctionalNode(Node):
    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, children):
        self._children = children
        for child in self._children:
            child.level = self.level + 1

    def add_child(self, child):
        child.level = self.level + 1
        self._children.add(child)

    def __init__(self):
        super().__init__()
        self._children = set()


class TerminalNode(Node):
    @property
    def children(self):
        raise AttributeError("Terminal node can not have children")
