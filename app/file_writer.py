"""Base class for JsonWriter and XmlWriter"""

from app.dragonfly import Dragonfly

from typing import Self, Any

class FileWriter:
    # gets data from dragonfly object
    def __init__(self: Self, dragonfly: Dragonfly):
        self.dragonfly: Dragonfly = dragonfly

    def get_data(self: Self, **kwargs):
        raise NotImplementedError()
    
    @staticmethod
    def save(data: Any, output_filename: str, min: bool):
        raise NotImplementedError()
