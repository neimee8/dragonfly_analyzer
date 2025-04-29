"""Base class for JsonWriter and XmlWriter"""

from app.dragonfly import Dragonfly

class FileWriter:
    # gets data from dragonfly object
    def __init__(self, dragonfly: Dragonfly):
        self.dragonfly = dragonfly

    def get_data(self, **kwargs):
        raise NotImplementedError()
    
    @staticmethod
    def save(data, output_filename: str, min: bool):
        raise NotImplementedError()
    