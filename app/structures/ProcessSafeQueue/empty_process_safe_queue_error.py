"""Exception raised when attempting to retrieve a value from an empty queue"""

from typing import Self

class EmptyProcessSafeQueueError(Exception):
    def __init__(self: Self, message: str = None) -> None:
        self.message = '<EmptyProcessSafeQueueError: '
        self.message += message if message else 'ProcessSafeQueue is empty!'
        self.message += '>'

        super().__init__(self.message)

    def __str__(self: Self) -> str:
        return self.message
    
    def __repr__(self: Self) -> str:
        return self.message
