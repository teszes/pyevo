from logging import getLogger
from random import choice, random

from pyevo.algorithms.bp import FunctionalNode, TerminalNode, Node

LOGGER = getLogger("pyevo.bp")


class TreeGenerator:

    def __init__(self,
                 max_width: int = None,
                 max_depth: int = None,
                 max_nodes: int = None,
                 max_children: int = None,
                 extension_probability: float = .99
                 ):
        self.max_width = max_width
        self.max_depth = max_depth
        self.max_nodes = max_nodes
        self.max_children = max_children
        self.extension_probability = extension_probability

    def __call__(self,
                 functionals: tuple = tuple(),
                 terminals: tuple = tuple()) -> Node:

        # Log tree generation
        LOGGER.debug(
            "Creating tree from {} functional and {} terminal templates".format(len(functionals), len(terminals)))

        # List of functionals that can receive additional children
        possible_parents = list()

        # Count of all nodes and nodes on each level of the tree
        node_count = 1
        level_populations = {1: 1}

        # Creating a tree root by taking a random function and building a node around it
        root_function = choice(functionals + terminals)
        root = FunctionalNode(root_function) if root_function in functionals else TerminalNode(root_function)

        # Check if root can have children
        if isinstance(root, FunctionalNode):
            possible_parents.append(root)

        # Tree extension loop
        while possible_parents \
                and (not self.max_nodes or node_count < self.max_nodes) \
                and (not self.extension_probability or random() < self.extension_probability):

            # Finding a prospective parent
            parent = choice(possible_parents)

            # Skip loop and remove parent from possible parents if there is no space for new children
            if self.max_children and not len(parent.children) < self.max_children:
                possible_parents.remove(parent)
                continue

            # Creating a prospective child
            child_function = choice(functionals + terminals)
            child = FunctionalNode(child_function) if child_function in functionals else TerminalNode(child_function)

            # First case, child is a functional node, still room or no limit on width and depth also for children
            if isinstance(child, FunctionalNode) \
                    and (not self.max_width or level_populations.get(parent.level + 1, 0) < self.max_width) \
                    and (not self.max_depth or parent.level < self.max_depth - 1 or not self.max_depth):

                # Add the child to the parent
                parent.add_child(child)

                # There is room for children depthwise, so it is possible parent
                possible_parents.append(child)

                # Set limit counters
                level_populations[parent.level + 1] = level_populations.get(parent.level + 1) or 1
                node_count += 1

            # Second case, still room or no limit on width and depth for node itself
            elif (not self.max_width or level_populations.get(parent.level + 1, 0) < self.max_width) \
                    and (not self.max_depth or parent.level < self.max_depth or not self.max_depth):

                # Add the child to the parent
                parent.add_child(child)

                # Set limit counters
                level_populations[parent.level + 1] = level_populations.get(parent.level + 1) or 1
                node_count += 1

            # Third case, node can not be extended
            else:
                continue

        # Return the root of the completed tree
        return root
