from collections import namedtuple
from datetime import datetime
from logging import getLogger
from typing import Any, Callable, List, Tuple

from .population import Population
from ._specimen import Specimen

LOGGER = getLogger("pyevo.algorithms.common")


class InitializationStrategy:
    def __init__(
            self,
            fitness_function: Callable[[Any], Any],
            task: Callable[[Any], Any],
            population_size: int = 100,
            functional_templates: Tuple[Callable[[Any], Any]] = None,
            terminal_templates: Tuple[Callable[[Any], Any]] = None
    ) -> None:
        LOGGER.debug("Initialization strategy with {} specimens".format(population_size))

        self._population_size = population_size
        self._functional_templates = functional_templates
        self._terminal_templates = terminal_templates
        self._fitness_function = fitness_function
        self._task = task

    def __call__(self) -> Tuple[Specimen]:
        LOGGER.info("Creating population of {} specimens".format(self._population_size))

        return tuple(
            Specimen(
                self._functional_templates,
                self._terminal_templates,
                self._fitness_function,
                self._task
            ) for _ in range(self._population_size)
        )


class EvolutionStrategy:
    def __init__(self, substrategies: tuple = None):
        if substrategies:
            def composite_strategy(population: Population) -> Population:
                new_population = population
                for strategy in substrategies:
                    new_population = strategy(new_population)
                return new_population

            self.__call__ = composite_strategy

    def __call__(self, population: Population):
        LOGGER.critical("Empty evolution strategy called")
        raise ValueError("Empty evolution strategy called")
