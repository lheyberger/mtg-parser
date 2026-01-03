#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://www.tcgplayer.com/content/magic-the-gathering/deck/Malcolm-and-Vial-Smasher/496887",
    "mocked_responses": [
        {
            "pattern": mtg_parser.utils.build_pattern('tcgplayer.com'),
            "response": "mock_tcgplayer.json",
        },
    ],
}


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.tcgplayer
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.tcgplayer.TcgplayerDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
