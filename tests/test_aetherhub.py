#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, mocked_responses', [
    [
        'https://aetherhub.com/Deck/thrasios-and-tymna---efficient',
        [{
            'pattern': r'https://aetherhub.com/Deck/(?!FetchMtgaDeckJson)',
            'response': 'mock_aetherhub_489549',
        }, {
            'pattern': r'https://aetherhub.com/Deck/FetchMtgaDeckJson',
            'response': 'mock_aetherhub_489549_json',
        }]
    ],
])
def test_parse_deck(requests_mock, src, mocked_responses):
    for mocked_response in mocked_responses:
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.aetherhub.parse_deck(src)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://aetherhub.com/Deck/thrasios-and-tymna---efficient',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.aetherhub.parse_deck(src)

    assert result and all(result)
