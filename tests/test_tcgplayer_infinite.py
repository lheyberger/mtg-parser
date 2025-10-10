#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://infinite.tcgplayer.com/magic-the-gathering/deck/Cat-Base/465171",
    "mocked_responses": [
        {
            "pattern": mtg_parser.utils.build_pattern('tcgplayer.com'),
            "response": "mock_tcgplayer_infinite.json",
        },
    ],
}


@pytest.mark.slow
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.tcgplayer.TcgplayerDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
