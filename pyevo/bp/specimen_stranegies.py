from random import choice, random

from pyevo.bp.nodes import FunctionalNode, TerminalNode


class TreeGenerator:

    def __init__(self,
                 functionals: tuple = None,
                 terminals: tuple = None,
                 max_width: int = None,
                 max_depth: int = None,
                 max_nodes: int = None,
                 max_children: int = None
                 ):
        self.functionals = functionals
        self.terminals = terminals
        self.max_width = max_width
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.max_children = max_children

    def __call__(self):
        # TODO Check type hinting for classes
        if self.functionals is None and self.terminals is None:
            raise ValueError("Tree can not be generated without nodes")

        parentable_functionals = list()

        node_count = int(1)
        level_populations = {1: 1}

        root = choice(self.functionals + self.terminals)()

        if isinstance(root, FunctionalNode):
            parentable_functionals.append(root)

        while parentable_functionals:
            parent = choice(parentable_functionals)
            child = choice(self.functionals + self.terminals)()

            if (self.max_width and level_populations[parent.level + 1] < self.max_width) \
                    and (self.max_depth and parent.level < self.max_depth - 1 or not self.max_depth) \
                    and isinstance(root, FunctionalNode):
                if len(parent.children) < self.max_children:
                    parent.add_child(child)
                else:
                    continue
                parentable_functionals.append(child)
                level_populations[parent.level + 1] = level_populations.get(parent.level + 1) or 1
                node_count += 1
            elif (self.max_width and level_populations.get(parent.level + 1) < self.max_width) \
                    and (self.max_depth and parent.level < self.max_depth or not self.max_depth):
                if len(parent.children) < self.max_children:
                    parent.add_child(child)
                else:
                    continue
                level_populations[parent.level + 1] = level_populations.get(parent.level + 1) or 1
                node_count += 1
            else:
                continue

            if self.max_nodes and not node_count < self.max_nodes:
                return root
        return root
