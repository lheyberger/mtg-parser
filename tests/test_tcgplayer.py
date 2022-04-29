#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1384198',
        r'https://.*?tcgplayer.com',
        'mock_tcgplayer_3-amigos',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.tcgplayer.parse_deck(src)
    result = list(result)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1384198',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.tcgplayer.parse_deck(src)
    result = list(result)

    assert result and all(result)
