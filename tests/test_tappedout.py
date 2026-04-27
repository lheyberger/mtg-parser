#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_URL = "https://tappedout.net/mtg-decks/mtg-parser-3-amigos/"


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.tappedout
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.tappedout.TappedoutDeckParser()
    result = parser.parse_deck(DECK_URL, http_client_facade)
    assert_deck_is_valid(result)
