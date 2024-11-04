import os
from abc import ABC, abstractmethod


class OutfileParent(ABC):
    def __init__(self, name, outfile_type, location):
        self._name = None
        self._outfile_type = None
        self._location = None

        self.name = name
        self.outfile_type = outfile_type
        self.location = location

    @abstractmethod
    def write_to_outfile(self, data_to_write):
        """Writes Data to outfile..."""
        pass

    @property
    def name(self):
        return self._location

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("location must be a non-empty string")
        self._location = value

    @property
    def outfile_type(self):
        return self._location

    @outfile_type.setter
    def outfile_type(self, value):
        text = value.lower()
        if text not in {"browser", "localdb", "csv"}:
            raise ValueError("Active must be either \"browser\", \"localdb\" or \"csv\".")
        self._location = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        if not isinstance(value, str) or not value:
            raise ValueError("location must be a non-empty string")
        self._location = value

