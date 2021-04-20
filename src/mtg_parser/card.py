#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser.utils import get_scryfall_url


def _filter_tags(tags):
    if not tags:
        return list()
    tags = filter(bool, tags)
    tags = map(str, tags)
    tags = map(str.lower, tags)
    return list(tags)


class Card:

    def __init__(
        self,
        name,
        quantity=1,
        extension=None,
        number=None,
        tags=None,
    ):
        self.name = name
        self.quantity = int(quantity)
        self.extension = extension
        self.number = number
        self.tags = _filter_tags(tags)
        self.scryfall_url = get_scryfall_url(
            name,
            extension,
            number
        )

    def __repr__(self):
        return '<Card: {}>'.format(' '.join(self._get_parts()))

    def __str__(self):
        return ' '.join(self._get_parts())

    def _get_parts(self):
        if self.quantity:
            yield '{}'.format(self.quantity)

        if self.name:
            yield '{}'.format(self.name)

        if self.extension:
            yield '({})'.format(self.extension)

        if self.number:
            yield '{}'.format(self.number)

        if self.tags:
            yield '[{}]'.format(', '.join(self.tags))

        if self.scryfall_url:
            yield '{}'.format(self.scryfall_url)
