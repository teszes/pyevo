from datetime import datetime
from logging import getLogger
from random import choice
from statistics import median
from typing import List, Tuple

from ._specimen import Specimen
from ..common import Population

LOGGER = getLogger("pyevo.bp")


class BacterialMutationStrategy:
    def __init__(self, clone_count: int = 10) -> None:
        LOGGER.debug("Bacterial mutation strategy with {} clones".format(clone_count))

        self._clone_count = clone_count

    def __call__(self, population: Population) -> Population:
        LOGGER.debug("Performing bacterial mutation")


        return tuple((specimen.bacterial_mutation(self._clone_count) for specimen in population))


class InfectionStrategy:
    def __init__(self, infection_count: int = 20) -> None:
        LOGGER.debug("Infection strategy with {} infections".format(infection_count))

        self._infection_count = infection_count

    def __call__(self, population: Population) -> Population:
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
