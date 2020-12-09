from logging import getLogger
from typing import Any, Callable, Tuple

from .population import Population
from .population_strategies import InitializationStrategy
from ...database import DatabaseConnector

LOGGER = getLogger("pyevo.algorithms.common")


def initialize_population(
        fitness_function: Callable[[Any], Any],
        task: Callable[[Any], Any],
        functional_templates: Tuple[Callable[[Any], Any]] = None,
        terminal_templates: Tuple[Callable[[Any], Any]] = None,
        population_size: int = 100,
        database_connector: DatabaseConnector = DatabaseConnector()
) -> Population:

    with database_connector as connector:
        connector.write_row()

    return Population(
        initialization_strategy=InitializationStrategy(
            fitness_function=fitness_function,
            task=task,
            population_size=population_size,
            functional_templates=functional_templates,
            terminal_templates=terminal_templates
        )
    )