#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import json
from tabulate import tabulate


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

    assert len(cards) == 100, f'There should be exactly 100 cards in an EDH deck (parsed {len(cards)})'


def mock_response(requests_mock, pattern, response, basedir='tests/mocks'):
    if response:
        matcher = re.compile(pattern)
        with open(os.path.join(basedir, response), 'r') as file:
            requests_mock.get(matcher, text=file.read())


def print_deck(deck):
    dataset = ({
        'Quantity': c.quantity,
        'Name': c.name,
        'Ext': c.extension,
        '#': c.number,
        'Tags': ', '.join(c.tags),
        'Scryfall Url': c.scryfall_url,
    } for c in deck)
    print(tabulate(dataset, headers='keys'))
    print('Unique Cards  -', len(deck))
    print('Total # Cards -', sum(c.quantity for c in deck))
