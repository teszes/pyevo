import logging

from pyevo.algorithms.bp import \
    InitializationStrategy, TerminationStrategy, BacterialMutationStrategy, InfectionStrategy

LOGGER = logging.getLogger("pyevo.bp")


class BacterialProgramming:

    @property
    def results(self):
        LOGGER.debug("Retrieving raw_results")
        return list(self._results)

    def __init__(self,
                 population,
                 fitness_function,
                 task=None,
                 functionals: tuple = None,
                 terminals: tuple = None,
                 termination_strategy=TerminationStrategy(),
                 bacterial_mutation_strategy=BacterialMutationStrategy(),
                 infection_strategy=InfectionStrategy()):

        LOGGER.debug(
            "Bacterial Programming with {} functionals and {} terminals".format(len(functionals), len(terminals))
        )

        self._results = list()
        if not functionals and not terminals:
            LOGGER.critical("Tree can not be generated without nodes")
            raise ValueError("Tree can not be generated without nodes")

        self._population = population

        self._termination_strategy = termination_strategy
        self._bacterial_mutation_strategy = bacterial_mutation_strategy
        self._infection_strategy = infection_strategy

    def run(self, database_connection_string: str = None) -> None:
        LOGGER.info("Starting Bacterial Programming")
        population = self._initialization_strategy()
        while not self._termination_strategy(population, self._results):
            LOGGER.info("Bacterial Programming - {} cycles complete - {:.3f} {:.3f} {:.3f}".format(
                len(self._results),
                self._results[-1].min_fitness,
                self._results[-1].avg_fitness,
                self._results[-1].max_fitness
            ))
            population = self._bacterial_mutation_strategy(population)
            population = self._infection_strategy(population)
