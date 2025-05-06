"""Process-Safe Queue class"""

from config import Config

from app.structures.ProcessSafeQueue.node import Node
from app.structures.ProcessSafeQueue.empty_process_safe_queue_error import EmptyProcessSafeQueueError

from typing import Any, Self

cnf = Config()

class ProcessSafeQueue:
    # initialization with shared memory data
    def __init__(self: Self, shared_list, shared_head, shared_tail, shared_lock) -> None:
        self._list = shared_list
        self._head = shared_head
        self._tail = shared_tail
        self._lock = shared_lock

    # puts after the tail index of the queue
    def put(self: Self, value: Any) -> None:
        # locks data while using to avoid conflicts
        with self._lock:
            new_index = len(self._list)

            if self.is_empty(lock = False):
                self._head.value = new_index
            else:
                self._list[self._tail.value].next = new_index

            self._tail.value = new_index

            self._list.append(Node(value))

    # gets from the head index of the queue
    def get_nowait(self: Self) -> Any:
        with self._lock:
            try:
                value = self.peek(lock = False)
            except EmptyProcessSafeQueueError:
                return None

            next_head_index = self._head.value + 1
            self._head.value = next_head_index if len(self._list) > next_head_index else -1

            if self._head.value == -1:
                self._tail.value = -1

            # cleaning up if too much unusable elements and queue is empty
            if self.is_empty(lock = False) and len(self._list) >= cnf.psq_max_elements_before_cleanup:
                self._cleanup()

            return value
        
    # shows first element without deleting
    def peek(self: Self, lock: bool = True) -> Any:
        if self.is_empty(lock = lock):
            raise EmptyProcessSafeQueueError()
        
        def peek_queue() -> Any:
            return self._list[self._head.value].value
        
        if lock:
            with self._lock:
                return peek_queue()
        else:
            return peek_queue()
                
    # gets size of queue
    def qsize(self: Self, lock: bool = True) -> int:
        def get_size() -> int:
            size = 0
            current_index = self._head.value

            while current_index != -1:
                size += 1
                current_index = self._list[current_index].next

            return size
        
        if lock:
            with self._lock:
                return get_size()
        else:
            return get_size()
    
    # check if empty
    def is_empty(self: Self, lock: bool = True) -> bool:
        if lock:
            with self._lock:
                return self.qsize() == 0
        else:
            return self.qsize(lock = False) == 0
    
    # garbage collection
    def _cleanup(self: Self) -> None:
        self._list[:] = []
        self._head.value = -1
        self._tail.value = -1
    
    # behavior when used len()
    def __len__(self: Self) -> int:
        return self.qsize()
