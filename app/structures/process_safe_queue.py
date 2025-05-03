"""Process-Safe Queue class"""

# exception if empty
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

# Process-Safe Queue
class ProcessSafeQueue:
    # initialization with shared memory data
    def __init__(self, shared_list, shared_head, shared_tail, shared_lock):
        self._list = shared_list
        self._head = shared_head
        self._tail = shared_tail
        self._lock = shared_lock

    # puts in the end of the shared list
    def put(self, item: any):
        # locks data while using to avoid conflicts
        with self._lock:
            self._list.append(item)

    # gets from the beggining of the shared list
    def get_nowait(self):
        with self._lock:
            if len(self._list) > 0:
                return self._list.pop(0)
            else:
                raise EmptyProcessSafeQueueError()
