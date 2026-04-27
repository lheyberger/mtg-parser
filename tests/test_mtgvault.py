#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_URL = "https://www.mtgvault.com/gorila/decks/mtgparser-3-amigos/"


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.mtgvault
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.mtgvault.MtgvaultDeckParser()
    result = parser.parse_deck(DECK_URL, http_client_facade)
    assert_deck_is_valid(result)
