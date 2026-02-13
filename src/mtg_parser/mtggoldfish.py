#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections.abc import Iterable
from html import unescape
from re import search
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MtggoldfishDeckParser']


class MtggoldfishDeckParser(OnlineDeckParser[str]):

    _PATTERN = build_pattern('mtggoldfish.com', r'/deck/(?P<deck_id>\d+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[str]:
        response = http_client.get(src, headers={'Accept': 'text/html'})
        soup = BeautifulSoup(response.text, features='html.parser')
        csrf_token = (soup.find('meta', attrs={'name': 'csrf-token'}) or {}).get('content')

        match = search(self._PATTERN, src)
        deck_id = match.group('deck_id') if match else None
        if not deck_id:
            return None # pragma: no cover
        url = f"https://www.mtggoldfish.com/deck/component?id={deck_id}"
        headers = {
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = http_client.get(url, headers=headers)
        return response.text


    def _parse_deck(self, deck: str) -> Optional[Iterable[Card]]:
        deck = deck.splitlines()[0]
        deck = deck.replace("\\'", "'").replace('\\"', '"').replace("\\/", "/").replace(r"\n", "")
        deck = unescape(deck)

        soup = BeautifulSoup(deck, features='html.parser')
        soup = soup.find('table', class_='deck-view-deck-table')
        soup = soup.find_all('tr', recursive=False)

        current_tag = None
        for row in soup:
            if 'deck-category-header' in row.attrs.get('class', []):
                category = row.text.lower()
                current_tag = next((tag for tag in ['commander', 'companion', 'sideboard'] if tag in category), None)
            else:
                columns = row.find_all('td')
                data_card_id = row.a.attrs.get('data-card-id') if row.a else ''
                match = search(r'\[(.*?)\]', data_card_id)
                extension = match.group(1).lower() if match else None
                yield Card(
                    name=columns[1].get_text(strip=True),
                    quantity=columns[0].get_text(strip=True),
                    extension=extension,
                    tags=[current_tag],
                )
