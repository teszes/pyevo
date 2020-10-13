import random


class AlgorithmicReverse:

    def __init__(self):
        self._task = tuple(random.randint(1, 1001) for _ in range(1000))

    @property
    def task(self):
        """The original array of which the reverse must be submitted

        This array contains 1000 integers ranging from 1 to 1000 inclusive which can be read as many times as needed and
        the reverse must be submitted as a solution. This value is generated at class initialization and regenerated
        each time a solution is submitted.
        """
        return self._task

    def submit_solution(self, solution):
        if len(solution) != 1000:
            return 0

        score = int()
        for element in zip(reversed(self._task), solution):
            if element[0] == element[1]:
                score += 1
        # Regenerate task
        return score / 1000
