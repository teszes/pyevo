from collections import namedtuple
from datetime import datetime
from heapq import nlargest
from operator import attrgetter
from logging import getLogger
from random import choice
from statistics import median
from typing import List, Tuple

from pyevo.bp._specimen import Specimen

Result = namedtuple("Result", ["ts", "generation", "min_fitness", "max_fitness", "avg_fitness"])

LOGGER = getLogger("pyevo.bp")


class InitializationStrategy:
    def __init__(self, population_size=100) -> None:
        LOGGER.debug("Initialization strategy with {} specimens".format(population_size))

        self._population_size = population_size
        self.functionals = None
        self.terminals = None
        self.fitness_function = None
        self.task = None

    def __call__(self) -> Tuple[Specimen]:
        LOGGER.info("Creating {} specimens".format(self._population_size))

        return tuple(Specimen(self.functionals, self.terminals, self.fitness_function, self.task)
                     for _ in range(self._population_size))


class TerminationStrategy:
    def __init__(self, max_generations: int = 200, fitness_threshold: float = 1.0) -> None:

        LOGGER.debug(
            "Termination strategy with {} max generations or {} fitness treshold".format(
                max_generations, fitness_threshold
            )
        )

        self._max_generations = max_generations
        self._fitness_threshold = fitness_threshold

    def __call__(self, population: Tuple[Specimen], results: List[Result]) -> bool:
        if self._max_generations and not len(results) < self._max_generations:
            LOGGER.info("Terminating at max generation count")
            return True

        for specimen in population:
            if not self._fitness_threshold > specimen.fitness:
                LOGGER.info("Terminating at fitness treshold")
                return True

        results.append(Result(
            ts=datetime.now(),
            generation=len(results) + 1,
            min_fitness=min(specimen.fitness for specimen in population),
            max_fitness=max(specimen.fitness for specimen in population),
            avg_fitness=sum(specimen.fitness for specimen in population) / len(population),
        ))

        LOGGER.debug("Extended resultset, current length {} rows, continuing iteration".format(len(results)))

        return False


class BacterialMutationStrategy:
    def __init__(self, clone_count: int = 10) -> None:
        LOGGER.debug("Bacterial mutation strategy with {} clones".format(clone_count))

        self._clone_count = clone_count

    def __call__(self, population: Tuple[Specimen]) -> Tuple[Specimen]:
        LOGGER.debug("Performing bacterial mutation")
        return tuple((specimen.bacterial_mutation(self._clone_count) for specimen in population))


class InfectionStrategy:
    def __init__(self, infection_count: int = 20) -> None:
        LOGGER.debug("Infection strategy with {} infections".format(infection_count))

        self._infection_count = infection_count

    def __call__(self, population: Tuple[Specimen]) -> Tuple[Specimen]:
        LOGGER.debug("Performing infection")

        sorted_population = sorted(population, key=lambda specimen: specimen.fitness)
        bad_part = sorted_population[:int(len(population) / 2)]
        good_part = sorted_population[int(len(population) / 2):]
        del sorted_population

        for infection in range(self._infection_count):
            choice(bad_part).infect(choice(good_part))

        return population


class MedianInfectionStrategy(InfectionStrategy):
    def __call__(self, population: Tuple[Specimen]) -> Tuple[Specimen]:

        LOGGER.debug("Performing infection")

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

        return population


class NoveltySearchStrategy:
    def __init__(self):
        self.novel_specimens = list()

    def __call__(self, population: Tuple[Specimen]) -> Tuple[Specimen]:
        self.novel_specimens.extend(nlargest(int(len(population) / 10), population, key=lambda specimen: specimen.novelty(population)))
        if len(self.novel_specimens) == len(population):
            novel_specimens = self.novel_specimens
            self.novel_specimens = list()
            return tuple(novel_specimens)
        else:
            return population
