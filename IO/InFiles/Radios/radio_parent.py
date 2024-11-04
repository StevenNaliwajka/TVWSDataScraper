from abc import ABC, abstractmethod


class RadioParent(ABC):
    def __init__(self, name, location):
        self.name = name
        self.location = location

    def push_data(self, key, value):
        if hasattr(self, key):
            attr = getattr(self, key)
            if isinstance(attr, list):
                attr.append(value)
            else:
                setattr(self, key, value)
        else:
            raise ValueError("Key not in Child Radio object.")

    def pull_data(self, key, value):
        if hasattr(self, key):
            value = getattr(self, key)
            avg = sum(value) / len(value)
            return avg
        else:
            raise ValueError("Key not in Child Radio object.")
