#!/usr/bin/env python

import re
from urllib.parse import quote_plus


__all__ = []


def _format_name(card_name):
    card_name = card_name.split()
    card_name = map(str.strip, card_name)
    card_name = filter(len, card_name)
    card_name = ' '.join(card_name)
    card_name = quote_plus(card_name)
    return card_name


def _format_extension(extension):
    return str(extension).strip().lower()


def _format_number(number):
    return quote_plus(str(number).strip())


def get_scryfall_url(name=None, extension=None, number=None):
    scryfall_url = 'https://api.scryfall.com/cards'

    if extension and number:
        scryfall_url += f"/{_format_extension(extension)}"
        scryfall_url += f"/{_format_number(number)}"
    elif name and extension:
        scryfall_url += '/named'
        scryfall_url += f"?set={_format_extension(extension)}"
        scryfall_url += f"&exact={_format_name(name)}"
    elif name:
        scryfall_url += '/named'
        scryfall_url += f"?exact={_format_name(name)}"
    return scryfall_url


def build_pattern(domain: str, path: str = '') -> str:
    scheme = r'^(?:https?://)?'
    subdomain = r'(?:[a-zA-Z0-9-]+\.)*'
    domain = re.escape(domain.rstrip('/'))
    path_sep = '' if path.startswith('/') else '/'
    return ''.join([
        scheme,
        subdomain,
        domain,
        path_sep,
        path,
    ])


def match_pattern(url: str, pattern: str) -> bool:
    return isinstance(url, str) and isinstance(pattern, str) and re.match(pattern, url)
