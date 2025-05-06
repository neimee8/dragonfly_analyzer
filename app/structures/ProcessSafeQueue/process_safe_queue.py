"""Process-Safe Queue class"""

from app.structures.ProcessSafeQueue.node import Node
from app.structures.ProcessSafeQueue.empty_process_safe_queue_error import EmptyProcessSafeQueueError

class ProcessSafeQueue:
    # initialization with shared memory data
    def __init__(self, shared_list, shared_head, shared_tail, shared_lock):
        self._list = shared_list
        self._head = shared_head
        self._tail = shared_tail
        self._lock = shared_lock

    # puts after the tail index of the queue
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

    # gets from the head index of the queue
    def get_nowait(self) -> any:
        with self._lock:
            try:
                value = self.peek()
            except EmptyProcessSafeQueueError:
                return None

            next_head_index = self._head.value + 1
            self._head.value = next_head_index if len(self._list) > next_head_index else -1

            if self._head.value == -1:
                self._tail.value = -1

            return value
        
    # shows first element without deleting
    def peek(self):
        if self.is_empty():
            raise EmptyProcessSafeQueueError()

        return self._list[self._head.value].value
                
    # gets size of queue
    def qsize(self) -> int:
        size = 0
        current_index = self._head.value

        while current_index != -1:
            size += 1
            current_index = self._list[current_index].next

        return size
    
    # check if empty
    def is_empty(self) -> bool:
        return self.qsize() == 0
    
    # behavior when used len()
    def __len__(self) -> int:
        return self.qsize()
