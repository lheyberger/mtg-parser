#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import respx_mock, mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1432015",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?.*?tcgplayer.com",
            "response": "mock_tcgplayer_3-amigos",
        }
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.tcgplayer.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.tcgplayer.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.tcgplayer.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
