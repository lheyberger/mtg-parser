#!/usr/bin/env python

from collections.abc import Iterable
from re import fullmatch, search, sub
from typing import Any, Optional
from selectolax.lexbor import LexborHTMLParser
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['TappedoutDeckParser']


class TappedoutDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('tappedout.net', r'/mtg-decks/(?P<deck_id>[a-zA-Z0-9-_]+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        match = search(self._PATTERN, src)
        deck_id = match.group("deck_id") if match else None
        if not deck_id:
            return None # pragma: no cover
        url = "https://tappedout.net/api/deck/widget/"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        params = {
            "deck": deck_id,
            "cols": 1,
        }
        response = http_client.post(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
        cards = {}
        tree = LexborHTMLParser(deck.get("board", ""))
        for boardlist in tree.css("ul.tappedout-boardlist"):
            prev_node = boardlist.prev
            while prev_node and prev_node.tag != "h3":
                prev_node = prev_node.prev
            tag = self._format_tag(prev_node.text() if prev_node else "")
            for card_li in boardlist.css("li.tappedout-member"):
                qty = int(card_li.child.text(strip=True).strip("x"))
                name = card_li.css_first("a").text(strip=True)
                cards[(name, qty)] = tag

        all_tags = set(cards.values())
        for (name, qty), tag in cards.items():
            if tag == "commander":
                final_tag = "commander"
            elif tag == "sideboard":
                final_tag = "companion" if "commander" in all_tags else "sideboard"
            else:
                final_tag = None
            yield Card(name, quantity=qty, tags=[final_tag])


    @classmethod
    def _format_tag(cls, tag: str) -> str:
        match = fullmatch(r'(.*?)(?:\s+\(\d+\))?', tag)
        base = match.group(1) if match else tag
        cleaned = sub(r"[^\w\s]", "", base).lower()
        return "_".join(part for part in cleaned.split() if part)
