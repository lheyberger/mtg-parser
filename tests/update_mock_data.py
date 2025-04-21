#!/usr/bin/env python

from bs4 import BeautifulSoup
from conftest import create_test_http_client
from utils import _to_json

import mtg_parser


def update_aetherhub_mock_data(http_client):
    result = http_client.get('https://aetherhub.com/Deck/mtg-parser-3-amigos').text
    with open('tests/mocks/mock_aetherhub_3-amigos', 'w', encoding="utf-8") as mock_file:
        mock_file.write(result)

    soup = BeautifulSoup(result, features='html.parser')
    element = soup.find(attrs={'data-deckid': True})
    deck_id = element['data-deckid']
    deck = http_client.get(
        'https://aetherhub.com/Deck/FetchMtgaDeckJson',
        params={
            'deckId': deck_id,
            'langId': 0,
            'simple': False,
        }
    ).json()
    with open('tests/mocks/mock_aetherhub_3-amigos_json', 'w', encoding="utf-8") as mock_file:
        mock_file.write(_to_json(deck))


def update_archidekt_mock_data(http_client):
    deck = mtg_parser.archidekt._download_deck(
        'https://www.archidekt.com/decks/1365846/',
        http_client,
    )
    with open('tests/mocks/mock_archidekt_1365846_small', 'w', encoding="utf-8") as mock_file:
        mock_file.write(_to_json(deck))


def update_deckstats_mock_data(http_client):
    deck = http_client.get('https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos')
    with open('tests/mocks/mock_deckstats_30198_2034245', 'w', encoding="utf-8") as mock_file:
        mock_file.write(deck.text)


def update_moxfield_mock_data(http_client):
    deck = mtg_parser.moxfield._download_deck(
        'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        http_client,
    )
    with open('tests/mocks/mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ', 'w', encoding="utf-8") as mock_file:
        mock_file.write(_to_json(deck))


def update_mtggoldfish_mock_data(http_client):
    response = http_client.get(
        'https://www.mtggoldfish.com/deck/3935836',
        headers={'Accept': 'text/html'}
    )
    with open('tests/mocks/mock_mtggoldfish_3-amigos', 'w', encoding="utf-8") as mock_file:
        mock_file.write(response.text)

    soup = BeautifulSoup(response.text, features='html.parser')
    csrf_token = (soup.find('meta', attrs={'name': 'csrf-token'}) or {}).get('content')
    url = 'https://www.mtggoldfish.com/deck/component?id=3935836'
    headers = {
        'X-CSRF-Token': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = http_client.get(url, headers=headers)
    with open('tests/mocks/mock_mtggoldfish_3-amigos_content', 'w', encoding="utf-8") as mock_file:
        mock_file.write(response.text)


def update_mtgjson_mock_data(http_client):
    deck = mtg_parser.mtgjson._download_deck(
        'https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json',
        http_client,
    )
    with open('tests/mocks/mock_mtgjson_breedlethality_cmd2.json', 'w', encoding="utf-8") as mock_file:
        mock_file.write(_to_json(deck))


def update_scryfall_mock_data(http_client):
    deck = mtg_parser.scryfall._download_deck(
        'https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b',
        http_client,
    )
    with open('tests/mocks/mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b', 'w', encoding="utf-8") as mock_file:
        mock_file.write(deck)


def update_tappedout_mock_data(http_client):
    deck = mtg_parser.tappedout._download_deck(
        'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
        http_client,
    )
    with open('tests/mocks/mock_tappedout_3-amigos', 'w', encoding="utf-8") as mock_file:
        mock_file.write(deck)


def update_tcgplayer_infinite_mock_data(http_client):
    deck = mtg_parser.tcgplayer_infinite._download_deck(
        'https://infinite.tcgplayer.com/magic-the-gathering/deck/Cat-Base/465171',
        http_client,
    )
    with open('tests/mocks/mock_tcgplayer_infinite.json', 'w', encoding="utf-8") as mock_file:
        mock_file.write(_to_json(deck))


def update_tcgplayer_mock_data(http_client):
    deck = mtg_parser.tcgplayer._download_deck(
        'https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1432015',
        http_client,
    )
    with open('tests/mocks/mock_tcgplayer_3-amigos', 'w', encoding="utf-8") as mock_file:
        mock_file.write(deck)


def update_mock_data():
    http_client = create_test_http_client()
    functions = [
        update_aetherhub_mock_data,
        update_archidekt_mock_data,
        update_deckstats_mock_data,
        update_moxfield_mock_data,
        update_mtggoldfish_mock_data,
        update_mtgjson_mock_data,
        update_scryfall_mock_data,
        update_tappedout_mock_data,
        update_tcgplayer_infinite_mock_data,
        update_tcgplayer_mock_data,
    ]
    for f in functions:
        print(f'Executing {f.__name__}...')
        f(http_client)


if __name__ == "__main__":
    update_mock_data()
