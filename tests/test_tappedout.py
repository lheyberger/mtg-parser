#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://tappedout.net/mtg-decks/mtg-parser-3-amigos/",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?tappedout.net",
            "response": "mock_tappedout_3-amigos",
        },
    ],
}


@pytest.mark.slow
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.tappedout.TappedoutDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
