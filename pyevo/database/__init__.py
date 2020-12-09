from logging import getLogger
from uuid import uuid4

LOGGER = getLogger("pyevo.database")


class DatabaseConnector:
    def __init__(self):
        LOGGER.debug("Initializing database connection")

        self._run_id = uuid4()

    def __enter__(self):
        LOGGER.info("Connecting to database")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOGGER.info("Closing database connection")

    def _initialize_database(self) -> None:
        LOGGER.debug("Initializing database")

    def write_row(
            self,
            stage_id: str,
            population_id: str,
            generation: int,
            population_size: int,
            min_fitness: float,
            avg_fitness: float,
            max_fitness: float
    ) -> None:
        LOGGER.debug("Writing row to database")
