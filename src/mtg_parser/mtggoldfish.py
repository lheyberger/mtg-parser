#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections.abc import Iterable
from html import unescape
from re import search
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MtggoldfishDeckParser']


class MtggoldfishDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('mtggoldfish.com', r'/deck/(?P<deck_id>\d+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        response = http_client.get(src, headers={'Accept': 'text/html'})
        soup = BeautifulSoup(response.text, features='html.parser')
        csrf_token = (soup.find('meta', attrs={'name': 'csrf-token'}) or {}).get('content')

        deck_id = search(self._PATTERN, src).group('deck_id')
        url = f"https://www.mtggoldfish.com/deck/component?id={deck_id}"
        headers = {
            'X-CSRF-Token': csrf_token,
            'X-Requested-With': 'XMLHttpRequest',
        }
        response = http_client.get(url, headers=headers)
        return response.text


    def _parse_deck(self, deck: str) -> Iterable[Card]:
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
                current_tag = next((tag for tag in ['commander', 'companion'] if tag in category), None)
            else:
                yield Card(
                    row.a.string.strip(),
                    row.td.string.strip(),
                    search(
                        r'\[(.*?)\]',
                        row.a.attrs.get('data-card-id'),
                    ).group(1).lower(),
                    tags=[current_tag],
                )
