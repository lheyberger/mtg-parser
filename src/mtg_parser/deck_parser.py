#!/usr/bin/env python

from collections.abc import Iterable
from typing import Any, Generic, Optional, TypeVar
from abc import ABC, abstractmethod
from mtg_parser.card import Card
from mtg_parser.utils import match_pattern


DeckType = TypeVar("DeckType")


class BaseParser(ABC):

    @abstractmethod
    def can_handle(self, src: str) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def parse_deck(self, src: str, http_client: Any = None) -> Optional[Iterable[Card]]:
        pass # pragma: no cover


class OnlineDeckParser(BaseParser, Generic[DeckType]):

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern


    def can_handle(self, src: str) -> bool:
        return match_pattern(src, self.pattern)


    def parse_deck(self, src: str, http_client: Any = None) -> Optional[Iterable[Card]]:
        if not self.can_handle(src):
            return None

        if not all(hasattr(http_client, method) for method in ('get', )):
            raise TypeError('http_client must implement a requests-compatible interface.')

        raw_deck = self._download_deck(src, http_client)
        if not raw_deck:
            raise RuntimeError(f"Failed to download deck from {src}")

        return self._parse_deck(raw_deck)


    @abstractmethod
    def _download_deck(self, src: str, http_client: Any) -> Optional[DeckType]:
        pass # pragma: no cover


    @abstractmethod
    def _parse_deck(self, deck: DeckType) -> Optional[Iterable[Card]]:
        pass # pragma: no cover
