#!/usr/bin/env python

import re

import pytest

import mtg_parser


@pytest.mark.parametrize(('parameters', 'expected'), [
    (
        [],
        'https://api.scryfall.com/cards',
    ),
    (
        [None],
        'https://api.scryfall.com/cards',
    ),
    (
        [None, None],
        'https://api.scryfall.com/cards',
    ),
    (
        [None, None, None],
        'https://api.scryfall.com/cards',
    ),
])
def test_get_scryfall_url_no_parameters(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize(('parameters', 'expected'), [
    (
        ['Minsc & Boo, Timeless Heroes'],
        'https://api.scryfall.com/cards/named?exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
    (
        ['Minsc & Boo, Timeless Heroes', None],
        'https://api.scryfall.com/cards/named?exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
])
def test_get_scryfall_url_name(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize(('parameters', 'expected'), [
    (
        ['Minsc & Boo, Timeless Heroes', 'clb'],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
    (
        ['Minsc & Boo, Timeless Heroes', 'CLB'],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
    (
        ['Minsc & Boo, Timeless Heroes', 'clb', None],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
    (
        ['Minsc & Boo, Timeless Heroes', 'CLB', None],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ),
])
def test_get_scryfall_url_name_set(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize(('parameters', 'expected'), [
    (
        ['Minsc & Boo, Timeless Heroes', 'clb', 285],
        'https://api.scryfall.com/cards/clb/285',
    ),
    (
        ['Minsc & Boo, Timeless Heroes', 'clb', '285'],
        'https://api.scryfall.com/cards/clb/285',
    ),
    (
        ['Hymn to Tourach', 'fem', '38a'],
        'https://api.scryfall.com/cards/fem/38a',
    ),
    (
        ['Arcane Signet', 'p30m', '1F★'],
        'https://api.scryfall.com/cards/p30m/1F%E2%98%85',
    ),
])
def test_get_scryfall_url_name_set_code(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.slow
@pytest.mark.parametrize('parameters', [
    ['Minsc & Boo, Timeless Heroes', ],
    ['Minsc & Boo, Timeless Heroes', 'clb'],
    ['Minsc & Boo, Timeless Heroes', 'CLB'],
    ['Minsc & Boo, Timeless Heroes', 'clb', 285],
    ['Minsc & Boo, Timeless Heroes', 'clb', '285'],
    ['Hymn to Tourach', ],
    ['Hymn to Tourach', 'fem'],
    ['Hymn to Tourach', 'fem', '38a'],
    ['Arcane Signet', ],
    ['Arcane Signet', 'p30m'],
    ['Arcane Signet', 'p30m', '1F★'],
])
def test_request_urls(test_http_client, parameters):
    url = mtg_parser.utils.get_scryfall_url(*parameters)

    test_http_client.get(url, timeout=10).raise_for_status()


@pytest.mark.parametrize('scheme', [
    '', 'http://', 'https://',
])
@pytest.mark.parametrize('subdomain', [
    '', 'www.', 'v2.api.',
])
@pytest.mark.parametrize('domain', [
    'test-domain.com',
])
@pytest.mark.parametrize('path_prefix', [
    '/decks/',
])
@pytest.mark.parametrize('deck_id', [
    '1234567890', 'abcdef',
])
@pytest.mark.parametrize('path_suffix', [
    '', '/', '/other', '?querystring', '/?querystring',
])
def test_build_and_match_pattern_succeeds(
    scheme: str,
    subdomain: str,
    domain: str,
    path_prefix: str,
    deck_id: str,
    path_suffix: str,
    ):
    url = ''.join([scheme, subdomain, domain, path_prefix, deck_id, path_suffix])
    pattern = mtg_parser.utils.build_pattern(domain, r'/decks/(?P<deck_id>[a-zA-Z0-9]+)/?')
    assert mtg_parser.utils.match_pattern(url, pattern)

    parsed_deck_id = re.search(pattern, url).group('deck_id')
    assert parsed_deck_id == deck_id


@pytest.mark.parametrize('url', [
    '', 42, None, 'http://', 'https://www.', 'https://www.testdomain.com',
    'testdomain.com', 'nottest-domain.com.com', 'test-do.main.com', 'test-domain.co.uk',
    'test-domain.com.fake.domain', 'www.not-test-domain.com',
    'www.not-test-domain.com/test', 'ssh://test-domain.com', 'ssh://not-test-domain.com',
])
@pytest.mark.parametrize('domain', [
    'test-domain.com',
])
def test_build_and_match_pattern_fails(url: str, domain: str):
    pattern = mtg_parser.utils.build_pattern(domain)
    assert not mtg_parser.utils.match_pattern(url, pattern)
