#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_URL = "https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ"


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.moxfield
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.moxfield.MoxfieldDeckParser()
    result = parser.parse_deck(DECK_URL, http_client_facade)
    assert_deck_is_valid(result)
