from logging import getLogger
from random import randint
from typing import Callable

LOGGER = getLogger("pyevo.gym")


class AlgorithmicIdentity:

    def __init__(self, task_length=10):
        LOGGER.info("Initializing algorithmic identity task with a length of {}".format(task_length))
        self._task_length = task_length
        self._reset_task()

    @property
    def task(self):
        """The tuple to submit as a solution

        This array contains 1000 integers ranging from 1 to 1000 inclusive which can be read as many times as needed and
        must be submitted as a solution. This value is generated at class initialization and regenerated each time a
        solution is submitted.
        """
        return self._task

    def submit_solution(self, solution: Callable) -> float:
        LOGGER.debug("Evaluating solution {}".format(solution))

        solution_string = solution(self.task)

        task_substrings = set()
        solution_substrings = set()

        solution_checked_length = min(len(solution_string), self._task_length)

        for substring_length in range(self._task_length):
            for substring_start in range(0, self._task_length - substring_length):
                task_substrings.add(self._task[substring_start:substring_start + substring_length + 1])

        for substring_length in range(solution_checked_length):
            for substring_start in range(0, solution_checked_length - substring_length):
                solution_substrings.add(solution_string[substring_start:substring_start + substring_length + 1])

        score = len(task_substrings.intersection(solution_substrings)) / len(task_substrings)

        self._reset_task()

        return score

    def _reset_task(self):
        self._task = tuple(randint(1, 1001) for _ in range(self._task_length))
        if len(set(self._task)) != self._task_length:
            self._reset_task()
