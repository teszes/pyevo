import logging
import sqlite3
import typing
import uuid

from . import _bacterial_programming
from . import _population_strategies
from ._population_strategies import Result

LOGGER = logging.getLogger("pyevo.bp")


def bacterial_programming(
        fitness_function: typing.Callable[[typing.Any], float],
        task: typing.Any = None,
        functionals: typing.Tuple[typing.Callable[[typing.Any], typing.Any]] = None,
        terminals: typing.Tuple[typing.Callable[[typing.Any], typing.Any]] = None,
        population_size: int = 100,
        max_generations: int = 500,
        fitness_treshold: float = 1.0,
        mutation_clone_count: int = 10,
        result_database_path: str = None
) -> typing.Optional[typing.Union[typing.List[Result]]]:
    db_create_table_statement = """
    CREATE TABLE IF NOT EXISTS results 
    (
        ts TIMESTAMP,
        run_id TEXT,
        generation INTEGER,
        min_fitness REAL,
        avg_fitness REAL,
        max_fitness REAL
    )
    """

    db_insert_statement = """
    INSERT INTO results 
    (
        ts,
        run_id,
        generation,
        min_fitness,
        avg_fitness,
        max_fitness
    )
    VALUES 
    (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
    )
    """

    run_id = str(uuid.uuid4())

    model = _bacterial_programming.BacterialProgramming(
        fitness_function=fitness_function,
        task=task,
        functionals=functionals,
        terminals=terminals,
        initialization_strategy=_population_strategies.InitializationStrategy(
            population_size=population_size
        ),
        termination_strategy=_population_strategies.TerminationStrategy(
            max_generations=max_generations,
            fitness_threshold=fitness_treshold
        ),
        bacterial_mutation_strategy=_population_strategies.BacterialMutationStrategy(
            clone_count=mutation_clone_count
        ),
        infection_strategy=_population_strategies.InfectionStrategy(
        )
    )

    model.run()

    db_connection = sqlite3.connect(result_database_path)
    db_connection.execute(db_create_table_statement)
    for line in model.results:
        db_connection.execute(
            db_insert_statement,
            (
                line.ts,
                run_id,
                line.generation,
                line.min_fitness,
                line.avg_fitness,
                line.max_fitness
            )
        )
    db_connection.commit()

    return model.results

