from node import Node

class HashTable:
    # Creates a new HashTable with a capacity of 128 slots
    def __init__(self, capacity=128):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    # Method for iterating over keys
    def keys(self):
        return self.__iter__()
        
    # Method for iterating over values
    def values(self):
        for node in self.table:
            current = node
            while current:
                yield current.value
                current = current.next  
    
    # Method for iterating over (key, value) pairs
    def items(self):
        for node in self.table:
            current = node
            while current:
                yield (current.key, current.value)
                current = current.next

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
            
        new_node = Node(key, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.size += 1
    
    # Get the value associated with a key
    def __getitem__(self, key):
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next
        raise KeyError(key)
    
    # Returns True if the key exists in the hash table (supports the 'in' operator)
    def __contains__(self, key):
        try:
            self.__getitem__(key)
            return True
        except KeyError:
            return False
        
    # Returns the number of elements in the hash table (supports the len() function)
    def __len__(self):
        return self.size
    
    # Default iteration method (iterates over keys)
    def __iter__(self):
        for node in self.table:
            current = node 
            while current:
                yield current.key
                current = current.next
