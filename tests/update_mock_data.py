#!/usr/bin/env python

import mtg_parser
from pathlib import Path
from conftest import create_http_client_facade
from test_aetherhub import DECK_INFO as aetherhub_deck_info
from test_archidekt import DECK_INFO as archidekt_deck_info
from test_deckstats import DECK_INFO as deckstats_deck_info
from test_moxfield import DECK_INFO as moxfield_deck_info
from test_mtggoldfish import DECK_INFO as mtggoldfish_deck_info
from test_mtgjson import DECK_INFO as mtgjson_deck_info
from test_scryfall import DECK_INFO as scryfall_deck_info
from test_tappedout import DECK_INFO as tappedout_deck_info
from test_tcgplayer_infinite import DECK_INFO as tcgplayer_infinite_deck_info
from test_tcgplayer import DECK_INFO as tcgplayer_deck_info


def update_mock_data():

    urls = [
        aetherhub_deck_info['url'],
        archidekt_deck_info['url'],
        deckstats_deck_info['url'],
        moxfield_deck_info['url'],
        mtggoldfish_deck_info['url'],
        mtgjson_deck_info['url'],
        scryfall_deck_info['url'],
        tappedout_deck_info['url'],
        tcgplayer_infinite_deck_info['url'],
        tcgplayer_deck_info['url'],
    ]

    http_client = create_http_client_facade()
    http_client.write_mocks_to(Path('tests/mocks'))
    for url in urls:
        print(f'Writing mock data for {url}...')
        mtg_parser.parse_deck(url, http_client)


if __name__ == "__main__":
    update_mock_data()
