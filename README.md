# mtg-parser

![PyPI](https://img.shields.io/pypi/v/mtg-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-parser)
![GitHub](https://img.shields.io/github/license/lheyberger/mtg-parser)

## How to install

	pip install mtg-parser


## Quick Start

`mtg_parser.parse_deck()` can parse any decklist (textual or online) but if for any reason you want the specialized version, here are the supported websites:
* aetherhub.com
* archidekt.com
* deckstats.net
* moxfield.com
* mtggoldfish.com
* scryfall.com
* tappedout.net
* tcgplayer.com


### From textual decklist

`mtg_parser` can parse textual decklists with either MTGO or MTGA format

	import mtg_parser
	
	decklist = """
		1 Atraxa, Praetors' Voice
		1 Imperial Seal
		1 Lim-Dûl's Vault
		1 Jeweled Lotus (CMR) 319
		1 Llanowar Elves (M12) 182
		3 Brainstorm #Card Advantage #Draw
	"""
	
	cards = mtg_parser.decklist.parse_deck(decklist)
	
	for card in cards:
		print(card)

### From aetherhub.com

`mtg_parser` can parse public decks from aetherhub.com

	import mtg_parser
	
	url = 'https://aetherhub.com/Deck/<deckname>'
	cards = mtg_parser.aetherhub.parse_deck(url)
	for card in cards:
		print(card)


### From archidekt.com

`mtg_parser` can parse public decks from archidekt.com

	import mtg_parser
	
	url = 'https://www.archidekt.com/decks/<deckid>/'
	cards = mtg_parser.archidekt.parse_deck(url)
	for card in cards:
		print(card)


### From deckstats.net

`mtg_parser` can parse public decks from deckstats.net

	import mtg_parser
	
	url = 'https://deckstats.net/decks/<userid>/<deckid>'
	cards = mtg_parser.deckstats.parse_deck(url)
	for card in cards:
		print(card)


### From moxfield.com

`mtg_parser` can parse public decks from moxfield.com

	import mtg_parser
	
	url = 'https://www.moxfield.com/decks/<deckid>'
	cards = mtg_parser.moxfield.parse_deck(url)
	for card in cards:
		print(card)


### From mtggoldfish.com

`mtg_parser` can parse public decks from mtggoldfish.com

	import mtg_parser
	
	url = 'https://www.mtggoldfish.com/deck/<deckid>'
	cards = mtg_parser.mtggoldfish.parse_deck(url)
	for card in cards:
		print(card)


### From scryfall.com

`mtg_parser` can parse public decks from scryfall.com

	import mtg_parser
	
	url = 'https://scryfall.com/<userid>/decks/<deckid>/'
	cards = mtg_parser.scryfall.parse_deck(url)
	for card in cards:
		print(card)


### From tappedout.net

`mtg_parser` can parse public decks from tappedout.net

	import mtg_parser
	
	url = 'https://tappedout.net/mtg-decks/<deckid>/'
	cards = mtg_parser.tappedout.parse_deck(url)
	for card in cards:
		print(card)


### From tcgplayer.com

`mtg_parser` can parse public decks from tcgplayer.com

	import mtg_parser
	
	url = 'https://decks.tcgplayer.com/magic/<deckpath>'
	cards = mtg_parser.tcgplayer.parse_deck(url)
	for card in cards:
		print(card)
