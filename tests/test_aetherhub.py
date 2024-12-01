#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


DECK_INFO = {
    "url": "https://aetherhub.com/Deck/mtg-parser-3-amigos",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?(www\.)?aetherhub.com/Deck/(?!FetchMtgaDeckJson)",
            "response": "mock_aetherhub_3-amigos",
        },
        {
            "pattern": r"(https?://)?(www\.)?aetherhub.com/Deck/FetchMtgaDeckJson",
            "response": "mock_aetherhub_3-amigos_json",
        },
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.aetherhub.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.aetherhub.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock():
    result = mtg_parser.aetherhub.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)
