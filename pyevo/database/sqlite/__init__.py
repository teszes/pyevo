import sqlite3

from .. import DatabaseConnector


class SqliteDatabaseConnector(DatabaseConnector):

    def __init__(self, connection_string: str):
        super().__init__()

        self._connection_string = connection_string
        self._connection = None

        with open("create_table.sql") as create_script:
            self._create_table_statement = create_script.read()

        with open("insert_line.sql") as insert_script:
            self._insert_into_statement = insert_script.read()

    def __enter__(self):
        super().__enter__()
        self._initialize_database()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self._connection.close()

    def _initialize_database(self) -> None:
        super()._initialize_database()
        self._connection = sqlite3.connect("".join(self._connection_string.split("://")[1:]))

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
        super().write_row(stage_id, population_id, generation, population_size, min_fitness, avg_fitness, max_fitness)
        self._connection.execute(
            sql=self._insert_into_statement,
            parameters=[self._run_id, stage_id, generation, population_size, min_fitness, avg_fitness, max_fitness]
        )
        self._connection.commit()
