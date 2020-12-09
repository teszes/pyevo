from typing import Tuple
from uuid import uuid4

from ._specimen import Specimen
from .population_strategies import EvolutionStrategy, InitializationStrategy


class Population:
    def __init__(
            self,
            initialization_strategy: InitializationStrategy = None,
            population: Tuple[Specimen] = None
    ):
        self._population_id = str(uuid4())

        self._population = population or initialization_strategy()

        self._generation = 0

    @property
    def population_id(self):
        return self._population_id

    @property
    def generation(self):
        return self._generation

    def evolve(
            self,
            strategy: EvolutionStrategy()
    ):
        return strategy(self)
