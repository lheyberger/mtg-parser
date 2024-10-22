#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
import random
import pytest
from requests import Session
from requests.adapters import HTTPAdapter, Retry
from tabulate import tabulate
from more_itertools import ilen


def _to_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(',', ':'))


def _yield_all_cards(cards):
    for card in cards:
        for _ in range(card.quantity):
            yield card


def assert_objects_are_equal(result, expected):
    assert _to_json(result) == _to_json(expected)


def assert_deck_is_valid(cards):
    cards = _yield_all_cards(cards)
    cards = list(cards)

    nb_cards = ilen(filter(lambda card: 'companion' not in card.tags, cards))
    assert nb_cards == 100, f'There should be exactly 100 cards in an EDH deck (parsed {len(cards)})'

    tags = set(['commander', 'companion'])
    command_zone = filter(lambda card: tags & card.tags, cards)
    nb_command_zone = ilen(command_zone)
    assert nb_command_zone >= 1, f'There should be at least 1 card in the command zone (parsed {nb_command_zone})'
    assert nb_command_zone <= 3, f'There should be no more than 3 cards in the command zone (parsed {nb_command_zone})'


def mock_response(requests_mock, pattern, response, basedir='tests/mocks'):
    if response:
        matcher = re.compile(pattern)
        with open(os.path.join(basedir, response), 'r', encoding="utf-8") as file:
            requests_mock.get(matcher, text=file.read())
        requests_mock.head(matcher, status_code=200)


def print_deck(deck):
    deck = list(deck)
    dataset = ({
        'Quantity': c.quantity,
        'Name': c.name,
        'Ext': c.extension,
        '#': c.number,
        'Tags': ', '.join(c.tags),
    } for c in deck)
    print(tabulate(dataset, headers='keys'))
    print('Unique Cards  -', len(deck))
    print('Total # Cards -', sum(c.quantity for c in deck))


@pytest.fixture
def requests_session():
    return create_requests_session()


def create_requests_session():
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session = Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    session.headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.1',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.3',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        ]),
    }
    return session
