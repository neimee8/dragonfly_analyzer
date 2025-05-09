"""Process-Safe Queue class"""

from config import Config

from app.structures.ProcessSafeQueue.node import Node
from app.structures.ProcessSafeQueue.empty_process_safe_queue_error import EmptyProcessSafeQueueError

from typing import Any, Self, Iterator
from multiprocessing.managers import ListProxy, ValueProxy

cnf = Config()

class ProcessSafeQueue:
    """Process-Safe Queue class - makes possible data exchange between processes"""

    # initialization with shared memory data
    def __init__(
        self: Self,
        shared_list: ListProxy,
        shared_head: ValueProxy,
        shared_tail: ValueProxy,
        shared_lock: Any
    ) -> None:
        """Initialize ProcessSafeQueue with shared list, head, tail and lock from multiprocessing.Manager()"""

        self._list = shared_list
        self._head = shared_head
        self._tail = shared_tail
        self._lock = shared_lock

    # puts after the tail index of the queue
    def put(self: Self, value: Any) -> None:
        """Puts data after the tail index"""

        # locks data while using to avoid conflicts
        with self._lock:
            new_index = len(self._list)

            if self.is_empty(lock = False):
                self._head.value = new_index
            else:
                node = self._list[self._tail.value]
                node.next = new_index

                self._list[self._tail.value] = node

            self._tail.value = new_index

            self._list.append(Node(value))

    # gets from the head index of the queue
    def get_nowait(self: Self) -> Any:
        """Gets data from the head index"""

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
        """Shows head index element without deleting"""

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
        """Returns queue size"""
    
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
        """Checks if queue is empty"""

        if lock:
            with self._lock:
                return self.qsize() == 0
        else:
            return self.qsize(lock = False) == 0
        
    # checks if the value is in the queue
    def contains(self: Self, item: Any) -> bool:
        """Checks if the given value is in the queue"""

        return self.__contains__(item)
    
    # clears the queue by request
    def clear(self: Self) -> None:
        """Clears the queue by request"""

        with self._lock:
            self._cleanup()
    
    # clears the queue
    def _cleanup(self: Self) -> None:
        """Clears the queue"""

        self._list[:] = []
        self._head.value = -1
        self._tail.value = -1
    
    # behavior when used len()
    def __len__(self: Self) -> int:
        """Returns the size of queue"""

        return self.qsize()
    
    # string represantation
    def __str__(self: Self) -> str:
        """Returns a string representation of the queue, showing all its elements"""

        with self._lock:
            out = ''

            if len(self._list) == 0:
                out += 'Empty'
            else:
                out += '[head]: '
                current_index = self._head.value

                while current_index != -1:
                    node = self._list[current_index]

                    if current_index == self._tail.value:
                        out += '[tail]: '

                    out += str(node.value) + f' (next = {node.next})'

                    if current_index < self._tail.value:
                        out += ' -> '

                    current_index = node.next

            return out
    
    # string representation
    def __repr__(self: Self) -> str:
        """Returns a string representation of the ProcessSafeQueue instance"""

        out = f'<{self.__class__.__name__}>: '
        out += self.__str__()

        return out
    
    # standart iterator
    def __iter__(self: Self) -> Iterator[Any]:
        """Iterates over the elements in the queue"""

        with self._lock:
            current_index = self._head.value
            
            while current_index != -1:
                node = self._list[current_index]
                yield node.value

                current_index = node.next

    # checks if the value is in the queue
    def __contains__(self: Self, item: Any) -> bool:
        """Checks if the given value is in the queue"""

        with self._lock:
            current_index = self._head.value

            while current_index != -1:
                node = self._list[current_index]

                if node.value == item:
                    return True
                
                current_index = node.next
                
            return False
