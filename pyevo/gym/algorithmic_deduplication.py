import random


class AlgorithmicDeduplication:

    def __init__(self):
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
        solution_set = set(solution)
        score = 1.0
        score *= len(solution_set) / len(solution)
        score *= len(solution_set.intersection(self._task)) / len(solution_set.union(self._task))
        self._reset_task()
        return score

    def _reset_task(self):
        self._task = tuple(random.randint(1, 1001) for _ in range(1000))
