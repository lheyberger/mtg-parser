#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests
import mtg_parser
from .utils import mock_response, assert_deck_is_valid, requests_session


DECK_INFO = {
    "url": "https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ",
    "mocked_responses": [
        {
            "pattern": r"(https?://)?.*?moxfield.com",
            "response": "mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ",
        }
    ],
}


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_can_handle_succdeeds(deck_info):
    result = mtg_parser.moxfield.can_handle(deck_info['url'])

    assert result


@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck(requests_mock, deck_info):
    for mocked_response in deck_info['mocked_responses']:
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.moxfield.parse_deck(deck_info['url'])

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('deck_info', [DECK_INFO])
def test_parse_deck_no_mock(requests_session, deck_info):
    result = mtg_parser.moxfield.parse_deck(deck_info['url'], requests_session)

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.moxfield.com/decks/KJGxdJIxAkqDnowdAjimdg',
])
def test_parse_deck_corner_cases_no_mock(requests_session, src):
    result = mtg_parser.moxfield.parse_deck(src, requests_session)

    for card in result:
        url = mtg_parser.utils.get_scryfall_url(card.name, card.extension, card.number)
        requests.get(url, timeout=10).raise_for_status()
