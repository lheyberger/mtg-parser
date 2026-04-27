#!/usr/bin/env python

import pytest
import mtg_parser
from pathlib import Path
from mtg_parser.card import Card
from .test_aetherhub import DECK_URL as aetherhub_deck_url
from .test_archidekt import DECK_URL as archidekt_deck_url
from .test_deckstats import DECK_URL as deckstats_deck_url
from .test_moxfield import DECK_URL as moxfield_deck_url
from .test_mtggoldfish import DECK_URL as mtggoldfish_deck_url
from .test_scryfall import DECK_URL as scryfall_deck_url
from .test_tappedout import DECK_URL as tappedout_deck_url


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


@pytest.mark.parametrize('deck_url', [
    aetherhub_deck_url,
    archidekt_deck_url,
    deckstats_deck_url,
    mtggoldfish_deck_url,
    scryfall_deck_url,
    tappedout_deck_url,
])
def test_diff_decks(http_client_facade, deck_url):
    """
        Not tested:
        - mtgjson: different than the other supported websites
        - tcgplayer: can't post a decklist on this site
    """
    http_client_facade.read_mocks_from(Path('tests/mocks'))

    deck1 = mtg_parser.parse_deck(moxfield_deck_url, http_client_facade)
    deck2 = mtg_parser.parse_deck(deck_url, http_client_facade)

    result = compare_decks(deck1, deck2)

    assert not result['deck1 - deck2']
    assert result['deck1 x deck2']
    assert not result['deck2 - deck1']
