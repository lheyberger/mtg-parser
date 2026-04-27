#!/usr/bin/env python

import mtg_parser
from pathlib import Path
from .conftest import create_http_client_facade
from .test_aetherhub import DECK_URL as aetherhub_deck_url
from .test_archidekt import DECK_URL as archidekt_deck_url
from .test_deckstats import DECK_URL as deckstats_deck_url
from .test_moxfield import DECK_URL as moxfield_deck_url
from .test_mtggoldfish import DECK_URL as mtggoldfish_deck_url
from .test_mtgjson import DECK_URL as mtgjson_deck_url
from .test_mtgvault import DECK_URL as mtgvault_deck_url
from .test_scryfall import DECK_URL as scryfall_deck_url
from .test_tappedout import DECK_URL as tappedout_deck_url
from .test_tcgplayer_infinite import DECK_URL as tcgplayer_infinite_deck_url
from .test_tcgplayer import DECK_URL as tcgplayer_deck_url


def update_mock_data():

    urls = [
        aetherhub_deck_url,
        archidekt_deck_url,
        deckstats_deck_url,
        moxfield_deck_url,
        mtggoldfish_deck_url,
        mtgjson_deck_url,
        mtgvault_deck_url,
        scryfall_deck_url,
        tappedout_deck_url,
        tcgplayer_infinite_deck_url,
        tcgplayer_deck_url,
    ]

    http_client = create_http_client_facade()
    http_client.write_mocks_to(Path('tests/mocks'))
    for url in urls:
        print(f'Writing mock data for {url}...')
        mtg_parser.parse_deck(url, http_client)


if __name__ == "__main__":
    update_mock_data()
