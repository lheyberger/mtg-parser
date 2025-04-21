#!/usr/bin/env python

import httpx
import pytest

import mtg_parser

from .utils import assert_deck_is_valid, mock_response


DECK_INFO = {
    "url": "https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?.*?moxfield.com",
            "response": "mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ",
        }
    ],
}


def test_can_handle_succdeeds():
    result = mtg_parser.moxfield.can_handle(DECK_INFO['url'])

    assert result


def test_parse_deck(respx_mock):
    for mocked_response in DECK_INFO['mocked_responses']:
        mock_response(
            respx_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.moxfield.parse_deck(DECK_INFO['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
def test_parse_deck_no_mock(test_http_client):
    result = mtg_parser.moxfield.parse_deck(DECK_INFO['url'], test_http_client)

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.moxfield.com/decks/KJGxdJIxAkqDnowdAjimdg',
])
def test_parse_deck_corner_cases_no_mock(test_http_client, src):
    result = mtg_parser.moxfield.parse_deck(src, test_http_client)

    for card in result:
        url = mtg_parser.utils.get_scryfall_url(card.name, card.extension, card.number)
        httpx.get(url, timeout=10).raise_for_status()
