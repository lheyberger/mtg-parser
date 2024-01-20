# mtg-parser

![PyPI](https://img.shields.io/pypi/v/mtg-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-parser)
![Github - Nightly Check](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/nightly.yaml?label=Nightly%20check)
![GitHub](https://img.shields.io/github/license/lheyberger/mtg-parser)

**mtg-parser** is a Python library to download and parse Magic The Gathering decklists. It supports the most popular decklists hosting websites.


## Table of contents

- [Installation](#installation)
- [Supported Formats](#supported-formats)
- [Known issues](#known-issues)
- [Usage](#usage)


## Installation

The following section covers the installation of **mtg-parser**.

Before using **mtg-parser**, you will need:
- python >= 3.8.1

To install **mtg-parser**, simply run one of the following commands in the terminal of your choice:

```shell
$ pip install mtg-parser
```

or

```shell
$ poetry add mtg-parser
```


## Supported Formats

In addition to [MTGO](mtgo.com) and [MTGA](magic.wizards.com/mtgarena) formats, **mtg-parser** supports the following websites:
- [aetherhub.com](aetherhub.com)
- [archidekt.com](archidekt.com)
- [deckstats.net](deckstats.net)
- [moxfield.com](moxfield.com)
- [mtggoldfish.com](mtggoldfish.com)
- [scryfall.com](scryfall.com)
- [tappedout.net](tappedout.net)
- [tcgplayer.com](tcgplayer.com)


## Known issues

### Moxfield

[moxfield.com](moxfield.com) prevents the scraping of their website (it's against their Terms of Service).
Please contact support@moxfield.com if you want to proceed anyway.


## Usage

Start by importing the Requests module:

```python
import requests
```

Now let's parse a decklist (in any of the supported formats) and display the cards:

```python
cards = mtg_parser.parse_deck(<url>)
for card in cards:
	print(card)
```

`mtg_parser.parse_deck()` is a shortcut method to the specialized versions.
Provided that `url` is a valid Moxfield url, the following lines are equivalent:

```python
cards = mtg_parser.parse_deck(url)
# is the same as:
cards = mtg_parser.moxfield.parse_deck(url)
```

If for any reason, you need to configure how **mtg-parser** is fetching remote decklists, you can provide an optional **session** object.

```python
from requests import Session

s = Session()
# Configure your session here
cards = mtg_parser.parse_deck(<url>, session=s)
for card in cards:
	print(card)
```

### Parsing textual decklist

`mtg_parser` can parse textual decklists in either MTGO or MTGA format

```python
import mtg_parser

decklist = """
	1 Atraxa, Praetors' Voice
	1 Imperial Seal
	1 Lim-Dûl's Vault
	1 Jeweled Lotus (CMR) 319
	1 Llanowar Elves (M12) 182
	3 Brainstorm #Card Advantage #Draw
"""

cards = mtg_parser.decklist.parse_deck(deck_list)
for card in cards:
	print(card)
```

### Parsing aetherhub.com decklists

`mtg_parser` can parse public decks from aetherhub.com

```python
import mtg_parser

url = 'https://aetherhub.com/Deck/<deck_name>'

cards = mtg_parser.aetherhub.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing archidekt.com decklists

`mtg_parser` can parse public decks from archidekt.com

```python
import mtg_parser

url = 'https://www.archidekt.com/decks/<deck_id>/'

cards = mtg_parser.archidekt.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing deckstats.net decklists

`mtg_parser` can parse public decks from deckstats.net

```python
import mtg_parser

url = 'https://deckstats.net/decks/<userid>/<deck_id>'

cards = mtg_parser.deckstats.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing moxfield.com decklists

`mtg_parser` can parse public decks from moxfield.com

```python
import mtg_parser

url = 'https://www.moxfield.com/decks/<deck_id>'

cards = mtg_parser.moxfield.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing mtggoldfish.com decklists

`mtg_parser` can parse public decks from mtggoldfish.com

```python
import mtg_parser

url = 'https://www.mtggoldfish.com/deck/<deck_id>'

cards = mtg_parser.mtggoldfish.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing scryfall.com decklists

`mtg_parser` can parse public decks from scryfall.com

```python
import mtg_parser

url = 'https://scryfall.com/<userid>/decks/<deck_id>/'

cards = mtg_parser.scryfall.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing tappedout.net decklists

`mtg_parser` can parse public decks from tappedout.net

```python
import mtg_parser

url = 'https://tappedout.net/mtg-decks/<deck_id>/'

cards = mtg_parser.tappedout.parse_deck(url)
for card in cards:
	print(card)
```


### Parsing tcgplayer.com decklists

`mtg_parser` can parse public decks from tcgplayer.com

```python
import mtg_parser

url = 'https://decks.tcgplayer.com/magic/<deck_path>'

cards = mtg_parser.tcgplayer.parse_deck(url)
for card in cards:
	print(card)
```
