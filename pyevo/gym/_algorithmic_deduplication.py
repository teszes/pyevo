from logging import getLogger
from random import randint
from typing import Callable

LOGGER = getLogger("pyevo.gym")


class AlgorithmicDeduplication:

    def __init__(self, task_length=10):
        LOGGER.info("Initializing algorithmic deduplication task with a length of {}".format(task_length))
        self._task_length = task_length
        self._reset_task()

    @property
    def task(self):
        """The tuple to deduplicate

        This array contains 1000 integers ranging from 1 to 1000 inclusive which can be read as many times as needed and
        the deduplicated set of its elements must be submitted. This value is generated at class initialization and
        regenerated each time a solution is submitted.
        """
        return self._task

    def submit_solution(self, solution):
        LOGGER.debug("Evaluating solution {}".format(solution))

        solution_string = solution(self.task)

        task_set = set(self._task)
        solution_set = set(solution_string)

        score = len(task_set.intersection(solution_set)) / len(task_set.union(solution_set))
        score *= len(task_set) / len(solution_string)

        self._reset_task()

        return score

    def _reset_task(self):
        self._task = tuple(randint(1, 1001) for _ in range(self._task_length))
        if len(set(self._task)) != self._task_length:
            self._reset_task()
