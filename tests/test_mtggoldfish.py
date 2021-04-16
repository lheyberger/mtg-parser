#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://www.mtggoldfish.com/deck/3862693',
        r'https://www.mtggoldfish.com',
        'mock_mtggoldfish_3862693',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.mtggoldfish.parse_deck(src)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.mtggoldfish.com/deck/3862693'
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.mtggoldfish.parse_deck(src)

    assert result and all(result)
