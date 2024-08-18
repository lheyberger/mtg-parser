#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?deckstats.net/",
            "response": "mock_deckstats_30198_2034245",
        }
    ],
}


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_can_handle_succdeeds(deck_info):
    result = mtg_parser.deckstats.can_handle(deck_info['url'])

    assert result


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck(requests_mock, deck_info):
    for mocked_response in deck_info['mocked_responses']:
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.deckstats.parse_deck(deck_info['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck_no_mock(deck_info):
    result = mtg_parser.deckstats.parse_deck(deck_info['url'])

    assert_deck_is_valid(result)
