#!/usr/bin/env python

from collections.abc import Iterable
from html import unescape
from re import search
from typing import Any, Optional
from selectolax.lexbor import LexborHTMLParser
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MtggoldfishDeckParser']


class MtggoldfishDeckParser(OnlineDeckParser[str]):

    _PATTERN = build_pattern('mtggoldfish.com', r'/deck/(?P<deck_id>\d+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[str]:
        match = search(self._PATTERN, src)
        deck_id = match.group("deck_id") if match else None
        if not deck_id:
            return None # pragma: no cover
        url = f"https://www.mtggoldfish.com/deck/component?id={deck_id}"
        headers = {
            "X-Requested-With": "XMLHttpRequest",
        }
        response = http_client.get(url, headers=headers)
        response.raise_for_status()
        return response.text


    def _parse_deck(self, deck: str) -> Optional[Iterable[Card]]:
        deck = deck.replace("\\'", "'").replace('\\"', '"').replace("\\/", "/").replace(r"\n", "")
        deck = unescape(deck)

        tree = LexborHTMLParser(deck)
        table = tree.css_first('table.deck-view-deck-table')

        current_tag = None
        for row in table.css('tr'):
            if 'deck-category-header' in row.attributes.get('class', ''):
                category = row.text().lower()
                current_tag = next((tag for tag in ('commander', 'companion', 'sideboard') if tag in category), None)
            else:
                columns = row.css('td')
                link = row.css_first('a')
                data_card_id = link.attributes.get('data-card-id', '') if link else ''
                match = search(r'\[(.*?)\]', data_card_id)
                extension = match.group(1).lower() if match else None
                yield Card(
                    name=columns[1].text(strip=True),
                    quantity=columns[0].text(strip=True),
                    extension=extension,
                    tags=[current_tag],
                )
