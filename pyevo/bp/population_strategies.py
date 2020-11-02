from collections import namedtuple
from random import choice
from statistics import median

from pyevo.bp.specimen import Specimen

Result = namedtuple("Result", ["generation", "min_fitness", "max_fitness", "avg_fitness"])


class InitializationStrategy:
    def __init__(self, population_size=100):
        self._population_size = population_size
        self.functionals = None
        self.terminals = None
        self.fitness_function = None
        self.task = None

    def __call__(self):
        return tuple(Specimen(self.functionals, self.terminals, self.fitness_function, self.task)
                     for _ in range(self._population_size))


class TerminationStrategy:
    def __init__(self, max_generations=200, fitness_threshold=1):
        self._max_generations = max_generations
        self._fitness_threshold = fitness_threshold

    def __call__(self, population, results):
        if not len(results) < self._max_generations:
            return True

        for specimen in population:
            if not self._fitness_threshold > specimen.fitness:
                return True

        results.append(Result(
            generation=len(results) + 1,
            min_fitness=min(specimen.fitness for specimen in population),
            max_fitness=max(specimen.fitness for specimen in population),
            avg_fitness=sum(specimen.fitness for specimen in population) / len(population),
        ))

        return False


class BacterialMutationStrategy:
    def __init__(self, clone_count=10):
        self._clone_count = clone_count

    def __call__(self, population):
        map(lambda specimen: specimen.bacterial_mutation(self._clone_count), population)


class InfectionStrategy:
    def __init__(self, infection_count=20):
        self._infection_count = infection_count

    def __call__(self, population):
        sorted_population = sorted(population, key=lambda specimen: specimen.fitness)
        bad_part = sorted_population[:int(len(population) / 2)]
        good_part = sorted_population[int(len(population) / 2):]
        del sorted_population

        for infection in range(self._infection_count):
            choice(bad_part).infect(choice(good_part))


class MedianInfectionStrategy(InfectionStrategy):
    def __call__(self, population):
        bad_part = list()
        good_part = list()
        median_fitness = median(specimen.fitness for specimen in population)

        for specimen in population:
            if specimen.fitness > median_fitness:
                good_part.append(specimen)
            else:
                bad_part.append(specimen)

        for infection in range(self._infection_count):
            choice(bad_part).infect(choice(good_part))
