#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?scryfall.com",
            "response": "mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b",
        },
    ],
}


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.scryfall
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.scryfall.ScryfallDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
