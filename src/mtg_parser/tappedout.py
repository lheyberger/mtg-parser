#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import defaultdict
import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.decklist import parse_deck as decklist_parse_deck


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'(?:https?://)?(?:www\.)?tappedout\.net/mtg-decks/', src)
    )


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    return session.get(src, params={'cat': 'custom'}).text


def _parse_deck(deck):
    soup = BeautifulSoup(deck, features='html.parser')

    tags = _find_tags(soup)

    cardlist = soup.find('textarea', id='mtga-textarea')
    cards = decklist_parse_deck(cardlist.get_text(strip=True))

    for card in cards:
        card.tags.update(tags.get(card.name, {}))
        yield card


def _find_tags(soup):
    tags = defaultdict(set)
    skipped_list = ['sideboard', 'other', ]

    boardlists = soup.find_all('ul', class_='boardlist')
    for boardlist in boardlists:
        tag = boardlist.find_previous_sibling('h3')
        tag = _format_tag(tag.text)
        if any(tag.startswith(skipped_tag) for skipped_tag in skipped_list):
            continue
        if tag == 'commanders':
            tag = 'commander'
        links = boardlist.find_all('a', class_='card-hover')
        card_names = [link['data-name'] for link in links]
        for card_name in card_names:
            tags[card_name].add(tag)

    return tags


def _format_tag(tag):
    tag = re.fullmatch(r'(.*?)\s\(\d+\)', tag).group(1)
    tag = re.sub(r'[^\w\s]', '', tag)
    tag = tag.lower()
    tag = tag.split()
    tag = map(str.strip, tag)
    tag = filter(len, tag)
    tag = '_'.join(tag)
    return tag
