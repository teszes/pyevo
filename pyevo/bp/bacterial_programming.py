from pyevo.bp.population_strategies import \
    InitializationStrategy, TerminationStrategy, BacterialMutationStrategy, InfectionStrategy


class BacterialProgramming:

    @property
    def results(self):
        return list(self._results)

    def __init__(self,
                 initialization_strategy=InitializationStrategy(),
                 termination_strategy=TerminationStrategy(),
                 bacterial_mutation_strategy=BacterialMutationStrategy(),
                 infection_strategy=InfectionStrategy()):
        self._results = list()
        self._initialization_strategy = initialization_strategy
        self._termination_strategy = termination_strategy
        self._bacterial_mutation_strategy = bacterial_mutation_strategy
        self._infection_strategy = infection_strategy

    def run(self):
        population = self._initialization_strategy()
        while not self._termination_strategy(population, self._results):
            self._bacterial_mutation_strategy(population)
            self._infection_strategy(population)
