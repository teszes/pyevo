from __future__ import annotations

from collections import namedtuple
from copy import deepcopy
from operator import attrgetter
from random import choice, randint

from pyevo.bp.specimen_stranegies import TreeGenerator


class Specimen:
    @property
    def fitness(self):
        self._fitness = self._fitness or self._submit(self._root(self._task))
        return self._fitness

    @property
    def family(self):
        return self._root.family

    @property
    def root(self):
        return self._root

    def __init__(self, submit, task=None, tree_generator=TreeGenerator()):
        self._fitness = None
        self._root = tree_generator()
        self._task = task
        self._submit = submit

    def bacterial_mutation(self, clone_count):
        Attempt = namedtuple("Attempt", ["tree", "fitness"])

        base_node = choice(self._root.family)
        for child_index in range(base_node.children):
            attempts = [Attempt(base_node.children[child_index], self.fitness)]

            for _ in range(clone_count):
                tree = TreeGenerator()()
                base_node.children = list(base_node.children).insert(child_index, tree)
                self._fitness = None
                attempts.append(Attempt(tree, self.fitness))

            base_node.children = \
                list(base_node.children).insert(child_index, max(attempts, key=attrgetter("fitness")).tree)

    def infect(self, other: Specimen):
        base_node = choice(self.family)
        other_node = choice(other.family)
        base_node.children = list(base_node.children).insert(randint(0, len(base_node.children)), deepcopy(other_node))
