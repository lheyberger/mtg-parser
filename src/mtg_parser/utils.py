#!/usr/bin/env python
# -*- coding: utf-8 -*-


__all__ = []


def scryfal_url_from_name(name):
    name = name.split()
    name = map(str.strip, name)
    name = filter(len, name)
    name = '+'.join(name)
    return 'https://api.scryfall.com/cards/named?fuzzy={}'.format(name)


def scryfal_url_from_extension(extension, collector_number):
    return 'https://api.scryfall.com/cards/{}/{}'.format(
        extension.lower(),
        collector_number.lower(),
    )
