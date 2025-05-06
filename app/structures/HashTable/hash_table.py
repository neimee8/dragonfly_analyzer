from app.structures.HashTable.node import Node

from collections.abc import Mapping    # for **kwargs
from typing import Dict, Union

class HashTable(Mapping):
    # Creates a new HashTable with a capacity of 128 slots
    def __init__(self, capacity=128, **kwargs): 
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity
        self.insertion_order = []

        for key, value in kwargs.items():
            self[key] = value

    # Method for iterating over keys
    def keys(self):
        return self.__iter__()
        
    # Method for iterating over values
    def values(self):
        for key in self.insertion_order:
            yield self[key]
    
    # Method for iterating over (key, value) pairs
    def items(self):
        for key in self.insertion_order:
            yield (key, self[key])

    # Method for removing an element by key 
    def pop(self, key): 
        index = self._hash(key) 
        previous = None
        current = self.table[index] 
  
        while current: 
            if current.key == key: 
                if previous: 
                    previous.next = current.next
                else: 
                    self.table[index] = current.next
                self.size -= 1
                self.insertion_order.remove(key)
                return
            previous = current 
            current = current.next
  
        raise KeyError(key) 
    
    # Hash function that maps a key to a table index
    def _hash(self, key):
        return hash(key) % self.capacity
    
    # Method for dynamic hash resizing
    def _resize(self):
        self.capacity = self.capacity * 2
        new_table = [None] * self.capacity

        for node in self.table:
            current = node
            while current:
                index = self._hash(current.key)
                new_node = Node(current.key, current.value)
                new_node.next = new_table[index]
                new_table[index] = new_node
                current = current.next

        self.table = new_table

    # Adds or updates a value associated with the given key
    def __setitem__(self, key, value):
        index = self._hash(key)
        current = self.table[index]

        while current:
            if current.key == key:
                current.value = value
                return
            current = current.next  

        # Resize if load factor exceeds 70%
        if (self.size + 1) > (self.capacity * 0.7):
            self._resize()
            index = self._hash(key)
        
        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1
        self.insertion_order.append(key)

    # Get the value associated with a key
    def __getitem__(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)
    
    # Returns the number of elements in the hash table (supports the len() function)
    def __len__(self):
        return self.size
    
    # Default iteration method (iterates over keys)
    def __iter__(self):
        for key in self.insertion_order:
            yield key

    # Check if HashTable contains a key
    def __contains__(self, key: Union[str, int]) -> bool:
        try:
            self[key]

            return True
        except KeyError:
            return False

    # Convert to a regular dictionary (recursive for deep convert) 
    def to_dict(self) -> Dict[any, any]:
        result = {}

        for key, value in self.items():

            if isinstance(value, HashTable):
                result[key] = value.to_dict()

            elif isinstance(value, dict):
                temp_dict = {}

                for sub_key, sub_value in value.items():
                    if isinstance(sub_value, HashTable):
                        temp_dict[sub_key] = sub_value.to_dict()
                    else:
                        temp_dict[sub_key] = sub_value

                result[key] = temp_dict

            elif isinstance(value, list):
                temp_list = []

                for item in value:
                    if isinstance(item, HashTable):
                        temp_list.append(item.to_dict())
                    else:
                        temp_list.append(item)

                result[key] = temp_list

            elif isinstance(value, tuple):
                temp_tuple = []

                for item in value:
                    if isinstance(item, HashTable):
                        temp_tuple.append(item.to_dict_recursive())
                    else:
                        temp_tuple.append(item)

                result[key] = tuple(temp_tuple)

            else:
                result[key] = value

        return result
