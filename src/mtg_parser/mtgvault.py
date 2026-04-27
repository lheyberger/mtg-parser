#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections.abc import Iterable
from re import search
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MtgvaultDeckParser']


class MtgvaultDeckParser(OnlineDeckParser[str]):

    _PATTERN = build_pattern('mtgvault.com', r'/([^/]+)/decks/([^/]+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[str]:
        response = http_client.get(src, headers={'Accept': 'text/html'})
        return response.text


    def _parse_deck(self, deck: str) -> Optional[Iterable[Card]]:
        sections = {
            'command-zone': ['commander'],
            'main-deck': [],
            'sideboard': ['companion'],
        }
        soup = BeautifulSoup(deck, features='html.parser')
        for section, tags in sections.items():
            section_node = soup.find('div', id=section)
            if section_node:
                for card_div in section_node.find_all('div', class_='deck-card'):
                    card = self._parse_card(card_div, tags)
                    if card:
                        yield card


    def _parse_card(self, card_div, tags) -> Optional[Card]:

        quantity_span = card_div.find('span')
        quantity_text = quantity_span.get_text(strip=True)
        quantity_match = search(r'(\d+)x', quantity_text)
        quantity = int(quantity_match.group(1)) if quantity_match else 1

        card_link = card_div.find('a')
        card_name = card_link.get('title', '')
        card_url = card_link.get('href', '')
        extension_match = search(r'/card/[^/]+/([^/]+)/', card_url)
        extension = extension_match.group(1) if extension_match else None

        return Card(
            name=card_name,
            quantity=quantity,
            extension=extension,
            tags=tags,
        )
