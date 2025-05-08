"""Exception raised when attempting to retrieve a value from an empty queue"""

from typing import Self

class EmptyProcessSafeQueueError(Exception):
    """Exception when queue is empty"""
    
    def __init__(self: Self, message: str = None) -> None:
        """Initializes the EmptyProcessSafeQueueError exception with a custom message if given"""

        self.message = '<EmptyProcessSafeQueueError: '
        self.message += message if message else 'ProcessSafeQueue is empty!'
        self.message += '>'

        super().__init__(self.message)

    def __str__(self: Self) -> str:
        """Returns a string representation of the exception"""

        return self.message
    
    def __repr__(self: Self) -> str:
        """Returns a string representation of the exception"""

        return self.message
