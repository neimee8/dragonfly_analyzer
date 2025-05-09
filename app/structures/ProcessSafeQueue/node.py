"""Node class used in ProcessSafeQueue, where the next element is referenced by index instead of a pointer due to multiprocessing"""

from dataclasses import dataclass
from typing import Any

@dataclass
class Node:
    """Stores data of queue element"""

    value: Any
    next: int = -1
