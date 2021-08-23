from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, Any, List


class IRecord(metaclass=ABCMeta):

    @abstractmethod
    def to_dict(self) -> Dict[Any, Any]:
        ...

    @abstractmethod
    def to_json(self) -> str:
        ...

    @abstractmethod
    def to_list(self) -> List[Any]:
        ...