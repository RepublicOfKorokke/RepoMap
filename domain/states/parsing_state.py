# domain/states/parsing_state.py
from dataclasses import dataclass
from typing import List

from domain.entities.code_tag import CodeTag


@dataclass(frozen=True)
class ParsingState:
    pass


@dataclass(frozen=True)
class Idle(ParsingState):
    pass


@dataclass(frozen=True)
class Processing(ParsingState):
    pass


@dataclass(frozen=True)
class Success(ParsingState):
    tags: List[CodeTag]


@dataclass(frozen=True)
class Error(ParsingState):
    message: str
