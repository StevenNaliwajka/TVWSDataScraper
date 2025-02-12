from abc import ABC, abstractmethod


class RadioParent(ABC):
    def __init__(self, name, ip):
        # Parent for the radios.
        self.name = name
        self.ip = ip