#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = []


def _format_name(card_name):
    card_name = card_name.split()
    card_name = map(str.strip, card_name)
    card_name = filter(len, card_name)
    card_name = '+'.join(card_name)
    return card_name


def _format_extension(extension):
    return str(extension).lower()


def _format_collector_number(collector_number):
    return str(collector_number).lower()


def get_scryfall_url(name=None, extension=None, collector_number=None):
    scryfall_url = 'https://api.scryfall.com/cards'

    if extension and collector_number:
        scryfall_url += '/{}/{}'.format(
            _format_extension(extension),
            _format_collector_number(collector_number),
        )
    elif name and extension:
        scryfall_url += '/named?set={}&fuzzy={}'.format(
            _format_extension(extension),
            _format_name(name),
        )
    elif name:
        scryfall_url += '/named?fuzzy={}'.format(
            _format_name(name),
        )

    return scryfall_url
