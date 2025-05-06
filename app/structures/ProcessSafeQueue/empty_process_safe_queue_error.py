"""Exception raised when attempting to retrieve a value from an empty queue"""

class EmptyProcessSafeQueueError(Exception):
    def __init__(self, message: str = None):
        self.message = '<EmptyProcessSafeQueueError: '
        self.message += message if message else 'ProcessSafeQueue is empty!'
        self.message += '>'

        super().__init__(self.message)

    def __str__(self):
        return self.message
    
    def __repr__(self):
        return self.message
