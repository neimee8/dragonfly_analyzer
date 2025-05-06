"""Process-Safe Queue class"""

from dataclasses import dataclass

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
    
@dataclass
class Node:
    value: any
    next: int = -1

# Process-Safe Queue (use of linked list structure is impossible due to queue usage in multiprocessing)
class ProcessSafeQueue:
    # initialization with shared memory data
    def __init__(self, shared_list, shared_head, shared_tail, shared_lock):
        self._list = shared_list
        self._head = shared_head
        self._tail = shared_tail
        self._lock = shared_lock

    # puts in the end of the shared list
    def put(self, value: any):
        # locks data while using to avoid conflicts
        with self._lock:
            new_index = len(self._list)

            if self.is_empty():
                self._head.value = new_index
            else:
                self._list[self._tail.value].next = new_index

            self._tail.value = new_index

            self._list.append(Node(value))

    # gets from the beggining of the shared list
    def get_nowait(self):
        with self._lock:
            if self.is_empty():
                raise EmptyProcessSafeQueueError()
            
            value = self._list[self._head.value].value

            next_head_index = self._head.value + 1
            self._head.value = next_head_index if len(self._list) > next_head_index else -1

            if self._head.value == -1:
                self._tail.value = -1

            return value
                
    def qsize(self):
        size = 0
        current_index = self._head.value

        while current_index != -1:
            size += 1
            current_index = self._list[current_index].next

        return size
    
    def is_empty(self):
        return self.qsize() == 0
