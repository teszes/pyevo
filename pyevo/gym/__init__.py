import logging

from . import _algorithmic_deduplication
from . import _algorithmic_identity
from . import _algorithmic_reverse

LOGGER = logging.getLogger("pyevo.gym")


def algorithmic_deduplication(task_length: int = 10) -> _algorithmic_deduplication.AlgorithmicDeduplication:
    return _algorithmic_deduplication.AlgorithmicDeduplication(
        task_length=task_length
    )


def algorithmic_identity(task_length: int = 10) -> _algorithmic_identity.AlgorithmicIdentity:
    return _algorithmic_identity.AlgorithmicIdentity(
        task_length=task_length
    )


def algorithmic_reverse(task_length: int = 10) -> _algorithmic_reverse.AlgorithmicReverse:
    return _algorithmic_reverse.AlgorithmicReverse(
        task_length=task_length
    )
