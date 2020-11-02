from random import choice, random

from pyevo.bp.nodes import FunctionalNode, TerminalNode, Node


class TreeGenerator:

    def __init__(self,
                 max_width: int = None,
                 max_depth: int = None,
                 max_nodes: int = None,
                 max_children: int = None
                 ):
        self.max_width = max_width
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.max_children = max_children

    def __call__(self,
                 functionals: tuple = None,
                 terminals: tuple = None) -> Node:

        parentable_functionals = list()

        node_count = int(1)
        level_populations = {1: 1}

        root_function = choice(functionals + terminals)
        root = FunctionalNode(root_function) if root_function in functionals else TerminalNode(root_function)

        if isinstance(root, FunctionalNode):
            parentable_functionals.append(root)

        while parentable_functionals:
            parent = choice(parentable_functionals)
            child_function = choice(functionals + terminals)
            child = FunctionalNode(child_function) if child_function in functionals else TerminalNode(child_function)

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
