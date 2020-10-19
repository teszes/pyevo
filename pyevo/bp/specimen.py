from pyevo.bp.specimen_stranegies import TreeGenerator


class Specimen:
    @property
    def fitness(self):
        self._fitness = self._fitness or self._submit(self._root(self._task))
        return self._fitness

    @property
    def root(self):
        return self._root

    def __init__(self, submit, task=None, tree_generator=TreeGenerator()):
        self._fitness = None
        self._root = tree_generator()
        self._task = task
        self._submit = submit

    def bacterial_mutation(self, clone_count):
        pass

    def infect(self, other):
        pass
