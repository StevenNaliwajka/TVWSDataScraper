from abc import ABC, abstractmethod


class RadioParent(ABC):
    def __init__(self, name):
        # Parent for the radios.
        self.name = name
