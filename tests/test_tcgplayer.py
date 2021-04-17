#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://decks.tcgplayer.com/magic/commander/playing-with-power-mtg/s08e08---kraum---tevesh/1383584',
        r'https://.*?tcgplayer.com',
        'mock_tcgplayer_s08e08_kraum_tevesh',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.tcgplayer.parse_deck(src)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
	'https://decks.tcgplayer.com/magic/commander/playing-with-power-mtg/s08e08---kraum---tevesh/1383584',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.tcgplayer.parse_deck(src)

    assert result and all(result)
