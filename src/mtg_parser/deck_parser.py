#!/usr/bin/env python

from typing import Any, Optional
from abc import ABC, abstractmethod
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.utils import match_pattern


class BaseParser(ABC):

    @abstractmethod
    def can_handle(self, src: str) -> bool:
        pass # pragma: no cover

    @abstractmethod
    def parse_deck(self, src: str, http_client: Any) -> Iterable[Card]:
        pass # pragma: no cover


class OnlineDeckParser(BaseParser):

    def __init__(self, pattern: str) -> None:
        self.pattern = pattern


    def can_handle(self, src: str) -> bool:
        return match_pattern(src, self.pattern)


    def parse_deck(self, src: str, http_client: Optional[Any] = None) -> Optional[Iterable[Card]]:
        if not self.can_handle(src):
            return None

        if not all(hasattr(http_client, method) for method in ('get', )):
            raise TypeError('http_client must implement a requests-compatible interface.')

        raw_deck = self._download_deck(src, http_client)
        if not raw_deck:
            raise RuntimeError(f"Failed to download deck from {src}")

        return self._parse_deck(raw_deck)


    @abstractmethod
    def _download_deck(self, src: str, http_client: Any) -> Optional[str]:
        pass # pragma: no cover


    @abstractmethod
    def _parse_deck(self, deck: str) -> Iterable[Card]:
        pass # pragma: no cover
