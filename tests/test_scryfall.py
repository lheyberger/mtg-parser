#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?scryfall.com",
            "response": "mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b",
        }
    ],
}


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_can_handle_succdeeds(deck_info):
    result = mtg_parser.scryfall.can_handle(deck_info['url'])

    assert result


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck(requests_mock, deck_info):
    for mocked_response in deck_info['mocked_responses']:
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.scryfall.parse_deck(deck_info['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck_no_mock(deck_info):
    result = mtg_parser.scryfall.parse_deck(deck_info['url'])

    assert_deck_is_valid(result)
