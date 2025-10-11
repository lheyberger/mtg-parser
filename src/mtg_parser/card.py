#!/usr/bin/env python

from collections.abc import Iterable


__all__ = ['Card']


def _format_extension(extension: str | None) -> str | None:
    if not extension:
        return extension
    return str(extension).strip()


def _format_number(number: str | None) -> str | None:
    if not number:
        return number
    return str(number).strip()


def _format_tags(tags: Iterable[str] | None) -> set[str]:
    if not tags:
        return set()
    tags = filter(bool, tags)
    tags = map(str, tags)
    tags = map(str.strip, tags)
    tags = filter(len, tags)
    tags = map(str.lower, tags)
    return set(tags)


class Card:

    def __init__(
        self,
        name: str,
        quantity: int = 1,
        extension: str | None = None,
        number: str | None = None,
        tags: Iterable[str] | None = None,
    ):
        self.name = name
        self.quantity = int(quantity)
        self.extension = _format_extension(extension)
        self.number = _format_number(number)
        self.tags = _format_tags(tags)

    def __repr__(self) -> str:
        return f"<Card: {' '.join(self._get_parts())}>"

    def __str__(self) -> str:
        return ' '.join(self._get_parts())

    def __eq__(self, other: 'Card') -> bool:
        return self._to_tuple() == other._to_tuple()

    def __ne__(self, other: 'Card') -> bool:
        return self._to_tuple() != other._to_tuple()

    def __lt__(self, other: 'Card') -> bool:
        return self._to_tuple() < other._to_tuple()

    def __le__(self, other: 'Card') -> bool:
        return self._to_tuple() <= other._to_tuple()

    def __gt__(self, other: 'Card') -> bool:
        return self._to_tuple() > other._to_tuple()

    def __ge__(self, other: 'Card') -> bool:
        return self._to_tuple() >= other._to_tuple()

    def _to_tuple(self) -> tuple[str, int, str | None, str | None, set[str]]:
        return (
            self.name,
            self.quantity,
            self.extension,
            self.number,
            self.tags,
        )

    def _get_parts(self) -> Iterable[str]:
        if self.quantity:
            yield f"{self.quantity}"

        if self.name:
            yield f"{self.name}"

        if self.extension:
            yield f"({self.extension})"

        if self.number:
            yield f"{self.number}"

        if self.tags:
            yield f"[{', '.join(self.tags)}]"
