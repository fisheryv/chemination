from abc import ABC, abstractmethod

import pygame


class Scene(ABC):
    def __init__(self, parent):
        self.parent = parent

    @abstractmethod
    def process_input(self, event: pygame.event.Event):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface):
        pass
