import logging

from pyevo.bp._population_strategies import \
    InitializationStrategy, TerminationStrategy, BacterialMutationStrategy, InfectionStrategy, NoveltySearchStrategy

LOGGER = logging.getLogger("pyevo.bp")


class BacterialProgramming:

    @property
    def results(self):
        LOGGER.debug("Retrieving raw_results")
        return list(self._results)

    def __init__(self,
                 fitness_function,
                 task=None,
                 functionals: tuple = None,
                 terminals: tuple = None,
                 initialization_strategy=InitializationStrategy(),
                 termination_strategy=TerminationStrategy(),
                 bacterial_mutation_strategy=BacterialMutationStrategy(),
                 novelty_search_strategy=NoveltySearchStrategy(),
                 infection_strategy=InfectionStrategy()):

        LOGGER.debug(
            "Bacterial Programming with {} functionals and {} terminals".format(len(functionals), len(terminals))
        )

        self._results = list()
        if not functionals and not terminals:
            LOGGER.critical("Tree can not be generated without nodes")
            raise ValueError("Tree can not be generated without nodes")

        initialization_strategy.functionals = functionals
        initialization_strategy.terminals = terminals
        initialization_strategy.fitness_function = fitness_function
        initialization_strategy.task = task
        self._initialization_strategy = initialization_strategy

        self._termination_strategy = termination_strategy
        self._bacterial_mutation_strategy = bacterial_mutation_strategy
        self._infection_strategy = infection_strategy
        self._novelty_search_strategy = novelty_search_strategy

    def run(self):
        LOGGER.info("Starting Bacterial Programming")
        population = self._initialization_strategy()
        while not self._termination_strategy(population, self._results):
            LOGGER.info("Bacterial Programming - {} cycles complete - {:.3f} {:.3f} {:.3f}".format(
                len(self._results),
                self._results[-1].min_fitness,
                self._results[-1].avg_fitness,
                self._results[-1].max_fitness
            ))
            population = self._novelty_search_strategy(population)
            population = self._bacterial_mutation_strategy(population)
            population = self._infection_strategy(population)
