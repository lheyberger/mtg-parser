#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?deckstats.net/",
            "response": "mock_deckstats_30198_2034245",
        },
    ],
}


@pytest.mark.slow
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.deckstats.DeckstatsDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
