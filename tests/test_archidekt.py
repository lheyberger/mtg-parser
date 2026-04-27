#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_URL = "https://www.archidekt.com/decks/1365846/"


@pytest.mark.slow
@pytest.mark.integration
@pytest.mark.archidekt
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.archidekt.ArchidektDeckParser()
    result = parser.parse_deck(DECK_URL, http_client_facade)
    assert_deck_is_valid(result)
