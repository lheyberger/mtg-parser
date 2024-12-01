#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import respx_mock, mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?scryfall.com",
            "response": "mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b",
        }
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.scryfall.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.scryfall.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.scryfall.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
