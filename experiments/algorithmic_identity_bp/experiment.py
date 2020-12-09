from functools import partial
from multiprocessing import Pool

from pyevo.database.sqlite import SqliteDatabaseConnector
from pyevo.gym import algorithmic_identity
from pyevo.algorithms.common import initialize_population
from pyevo.algorithms.bp import bacterial_programming

PROCESS_POOL_SIZE = 6
TASK_LENGTH = 10
POPULATION_SIZE = 100
MAX_GENERATIONS = 500
FITNESS_TRESHOLD = 1.0
MUTATION_CLONE_COUNT = 10
RUN_COUNT = 100
RESULT_DATABASE_PATH = 'results.db'

validation_model = algorithmic_identity(task_length=TASK_LENGTH)

terminals = tuple()
for number in range(TASK_LENGTH):
    terminal = partial(lambda task, _n: (task[_n], ), _n=number)
    terminals += (terminal, )

functionals = (
    lambda task, children: tuple([y for x in children for y in x]),
)


def run(_):
    database_connector = SqliteDatabaseConnector()
    bacterial_programming = bacterial_programming(
        max_generations=MAX_GENERATIONS,
        fitness_treshold=FITNESS_TRESHOLD,
        mutation_clone_count=MUTATION_CLONE_COUNT,
        database_connector=database_connector
    )

    population = initialize_population(
        fitness_function=validation_model.submit_solution,
        task=validation_model.task,
        functional_templates=functionals,
        terminal_templates=terminals,
        population_size=100,
        database_connector=database_connector
    )

    population.evolve(bacterial_programming)


Pool(PROCESS_POOL_SIZE).map(run, range(RUN_COUNT))
