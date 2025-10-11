#!/usr/bin/env python

import pytest
import mtg_parser
from pathlib import Path
from mtg_parser.card import Card
from .test_aetherhub import DECK_INFO as aetherhub_deck_info
from .test_archidekt import DECK_INFO as archidekt_deck_info
from .test_deckstats import DECK_INFO as deckstats_deck_info
from .test_moxfield import DECK_INFO as moxfield_deck_info
from .test_mtggoldfish import DECK_INFO as mtggoldfish_deck_info
from .test_scryfall import DECK_INFO as scryfall_deck_info
from .test_tappedout import DECK_INFO as tappedout_deck_info


def compare_decks(deck1, deck2, differences_only=False):
    def _format_name(card_name):
        return card_name.split('//')[0].strip()

    deckset1 = set(_format_name(card.name) for card in deck1)
    deckset2 = set(_format_name(card.name) for card in deck2)

    result = {}
    result['deck1 - deck2'] = deckset1.difference(deckset2)
    if not differences_only:
        result['deck1 x deck2'] = deckset1.intersection(deckset2)
    result['deck2 - deck1'] = deckset2.difference(deckset1)
    return result


@pytest.mark.parametrize(('deck1', 'deck2'), [
    (
        [
            Card('Brainstorm'),
            Card('Portent'),
            Card('Ponder'),
        ],
        [
            Card('Portent'),
            Card('Ponder'),
            Card('Opt'),
        ],
    ),
])
def test_diff(deck1, deck2):
    result = compare_decks(deck1, deck2)

    for _, value in result.items():
        assert value
        assert all(value)


@pytest.mark.parametrize('deck_info', [
    aetherhub_deck_info,
    archidekt_deck_info,
    deckstats_deck_info,
    mtggoldfish_deck_info,
    scryfall_deck_info,
    tappedout_deck_info,
])
def test_diff_decks(http_client_facade, deck_info):
    """
        Not tested:
        - mtgjson: different than the other supported websites
        - tcgplayer: can't post a decklist on this site
    """
    http_client_facade.read_mocks_from(Path('tests/mocks'))

    deck1 = mtg_parser.parse_deck(moxfield_deck_info['url'], http_client_facade)
    deck2 = mtg_parser.parse_deck(deck_info['url'], http_client_facade)

    result = compare_decks(deck1, deck2)

    assert not result['deck1 - deck2']
    assert result['deck1 x deck2']
    assert not result['deck2 - deck1']
