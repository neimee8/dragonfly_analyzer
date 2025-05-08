"""Base class for JsonWriter and XmlWriter"""

from app.dragonfly import Dragonfly

from typing import Self, Any, Union, Dict
import xml.etree.ElementTree as et

class FileWriter:
    """Preparing data and writing it to result file"""

    # gets data from dragonfly object
    def __init__(self: Self, dragonfly: Dragonfly) -> None:
        """Data load out of Dragonfly onject"""

        self.dragonfly: Dragonfly = dragonfly

    def get_data(self: Self, **kwargs) -> Union[et.Element, Dict[str, Any]]:
        """Returns prepaired data"""

        raise NotImplementedError()
    
    @staticmethod
    def save(data: Any, output_filename: str, min: bool) -> None:
        """Saves data to result file"""

        raise NotImplementedError()
