from logging import getLogger
from typing import Any, Callable, List, Tuple

from ..common.population import Population
from ._specimen import Specimen

LOGGER = getLogger("pyevo.algorithms.common")


class EvolutionStrategy:
    def __init__(self, strategies: dict = None):
        LOGGER.critical("Empty evolution strategy created")
        raise ValueError("Empty evolution strategy created")

    def __call__(self, population: Population):
        LOGGER.critical("Empty evolution strategy called")
        raise ValueError("Empty evolution strategy called")
