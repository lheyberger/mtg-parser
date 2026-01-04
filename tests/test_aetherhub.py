#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://aetherhub.com/Deck/mtg-parser-3-amigos",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?aetherhub.com/Deck/(?!FetchMtgaDeckJson)",
            "response": "mock_aetherhub_3-amigos",
        },
        {
            "pattern": r"(https?://)?(www\.)?aetherhub.com/Deck/FetchMtgaDeckJson",
            "response": "mock_aetherhub_3-amigos_json",
        },
    ],
}


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.aetherhub
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.aetherhub.AetherhubDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
