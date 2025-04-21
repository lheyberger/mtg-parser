#!/usr/bin/env python

import pytest

import mtg_parser

from .utils import assert_deck_is_valid, mock_response


DECK_INFO = {
    "url": "https://tappedout.net/mtg-decks/mtg-parser-3-amigos/",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?tappedout.net",
            "response": "mock_tappedout_3-amigos",
        }
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.tappedout.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.tappedout.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.tappedout.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
