from abc import ABC, abstractmethod


class Scene(ABC):
    def __init__(self, parent):
        self.parent = parent

    @abstractmethod
    def process_input(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen):
        pass
