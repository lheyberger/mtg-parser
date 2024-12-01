#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import respx_mock, mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://infinite.tcgplayer.com/magic-the-gathering/deck/Cat-Base/465171",
    "mocked_responses": [
        {
            "pattern": mtg_parser.utils.build_pattern('tcgplayer.com'),
            "response": "mock_tcgplayer_infinite.json",
        }
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.tcgplayer_infinite.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.tcgplayer_infinite.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.tcgplayer_infinite.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
