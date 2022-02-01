from abc import ABCMeta, abstractmethod
from typing import Dict, Optional


class Renderer(metaclass=ABCMeta):
    @abstractmethod
    def render(self, template: str, context: Optional[Dict[str, str]] = None):
        pass
