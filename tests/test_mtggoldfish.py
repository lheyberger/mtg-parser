#!/usr/bin/env python

import pytest

import mtg_parser

from .utils import assert_deck_is_valid, mock_response


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


def test_can_handle_succdeeds():
    result = mtg_parser.mtggoldfish.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.mtggoldfish.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.mtggoldfish.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
