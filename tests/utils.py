#!/usr/bin/env python

import json
import os
import re

from more_itertools import ilen
from tabulate import tabulate


NB_CARDS = 100
MIN_COMMANDERS = 1
MAX_COMMANDERS = 3


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
    assert nb_cards == NB_CARDS, f"There should be exactly {NB_CARDS} cards in an EDH deck (parsed {len(cards)})"

    tags = set(['commander', 'companion'])
    command_zone = filter(lambda card: tags & card.tags, cards)
    nb_command_zone = ilen(command_zone)
    assert nb_command_zone >= MIN_COMMANDERS, f"Wrong number of cards in the command zone ({nb_command_zone})"
    assert nb_command_zone <= MAX_COMMANDERS, f"Wrong number of cards in the command zone ({nb_command_zone})"


def mock_response(respx_mock, pattern, response, basedir='tests/mocks'):
    if not response:
        return
    with open(os.path.join(basedir, response), encoding="utf-8") as file:
        body = file.read()
    matcher = re.compile(pattern)
    respx_mock.get(matcher).respond(status_code=200, text=body)
    respx_mock.head(matcher).respond(status_code=200)


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
