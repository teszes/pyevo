import logging
import sqlite3
import typing
import uuid

from . import _bacterial_programming
from . import evolution_steps
from .evolution_steps import BacterialEvolutionStrategy

LOGGER = logging.getLogger("pyevo.bp")


def bacterial_programming(
        max_generations: int = 500,
        fitness_treshold: float = 1.0,
        mutation_clone_count: int = 10,
        database_connection_string: str = None
) -> EvolutionStrategy:

