#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://www.archidekt.com/decks/1365846/",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?archidekt.com/",
            "response": "mock_archidekt_1365846_small",
        },
    ],
}


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.archidekt
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.archidekt.ArchidektDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
