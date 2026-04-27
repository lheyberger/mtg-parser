#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_URL = "https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json"


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.mtgjson
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.mtgjson.MtgjsonDeckParser()
    result = parser.parse_deck(DECK_URL, http_client_facade)
    assert_deck_is_valid(result)
