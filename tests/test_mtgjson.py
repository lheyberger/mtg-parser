#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?mtgjson\.com",
            "response": "mock_mtgjson_breedlethality_cmd2.json",
        },
    ],
}


@pytest.mark.slow
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.mtgjson.MtgjsonDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
