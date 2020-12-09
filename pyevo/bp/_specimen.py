from __future__ import annotations

from collections import namedtuple
from copy import deepcopy
from operator import attrgetter
from random import choice, randint

from pyevo.bp._specimen_strategies import TreeGenerator


class Specimen:
    @property
    def fitness(self):
        self._fitness = self._fitness or self._fitness_function(self._root)
        return self._fitness

    @property
    def family(self):
        return self._root.family

    @property
    def root(self):
        return self._root

    def __init__(self, functionals, terminals, fitness_function, task=None, tree_generator=TreeGenerator()):
        self._fitness = None
        self._root = tree_generator(functionals=functionals, terminals=terminals)
        self._task = task
        self._fitness_function = fitness_function
        self._functionals = functionals
        self._terminals = terminals

    def bacterial_mutation(self, clone_count) -> Specimen:
        Attempt = namedtuple("Attempt", ["tree", "fitness"])

        base_node = choice(self._root.family)

        if not base_node.children:
            return self

        for child_index, _ in enumerate(base_node.children):
            attempts = [Attempt(base_node.children[child_index], self.fitness)]

            for _ in range(clone_count):
                tree = TreeGenerator()(self._functionals, self._terminals)
                list(base_node.children).insert(child_index, tree)
                self._fitness = None
                attempts.append(Attempt(tree, self.fitness))

            list(base_node.children).insert(child_index, max(attempts, key=attrgetter("fitness")).tree)

        return self

    def infect(self, other: Specimen) -> Specimen:
        base_node = choice(self.family)
        other_node = choice(other.family)
        list(base_node.children).insert(randint(0, len(base_node.children)), deepcopy(other_node))
        return self
