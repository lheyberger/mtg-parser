#!/usr/bin/env python

import pytest
import mtg_parser
from .utils import assert_deck_is_valid


DECK_INFO = {
    "url": "https://www.mtggoldfish.com/deck/3935836",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?mtggoldfish.com/deck/(?!component)",
            "response": "mock_mtggoldfish_3-amigos",
        },
        {
            "pattern": r"(https?://)?(www\.)?mtggoldfish.com/deck/component",
            "response": "mock_mtggoldfish_3-amigos_content",
        },
    ],
}


@pytest.mark.slow
def test_parse_deck_no_mock(http_client_facade):
    parser = mtg_parser.mtggoldfish.MtggoldfishDeckParser()
    result = parser.parse_deck(DECK_INFO['url'], http_client_facade)
    assert_deck_is_valid(result)
