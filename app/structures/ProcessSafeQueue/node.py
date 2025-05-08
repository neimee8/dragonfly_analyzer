"""Node class used in ProcessSafeQueue, where the next element is referenced by index instead of a pointer due to multiprocessing"""

from dataclasses import dataclass

@dataclass
class Node:
    """Stores data of queue element"""

    value: any
    next: int = -1
