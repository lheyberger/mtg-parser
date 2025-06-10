# mtg-parser

![PyPI](https://img.shields.io/pypi/v/mtg-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-parser)
![Github - Nightly Check](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/nightly.yaml?label=Nightly%20check)
![GitHub](https://img.shields.io/github/license/lheyberger/mtg-parser)

`mtg_parser` is a Python library to download and parse Magic: The Gathering decklists.
It supports the MTGO/MTGA formats as well as the most popular deck building websites.


## Table of contents

- [Installation](#installation)
- [Supported Formats](#supported-formats)
- [Known issues](#known-issues)
- [Usage](#usage)


## Installation

The following section covers the installation of `mtg_parser`.

Before using `mtg_parser`, you will need:
- `python >= 3.9`

To install `mtg_parser`, simply run one of the following commands in the terminal of your choice:

```shell
$ pip install mtg-parser
```

or

```shell
$ poetry add mtg-parser
```


## Supported Formats

> [!NOTE]
> `mtg_parser` has been developed with a primary *focus on Commander*.
> While it may function with other formats, compatibility is not guaranteed.


In addition to [MTGO](mtgo.com) and [MTGA](magic.wizards.com/mtgarena) formats, `mtg_parser` supports the following websites:
- [aetherhub.com](aetherhub.com)
- [archidekt.com](archidekt.com)
- [deckstats.net](deckstats.net)
- [moxfield.com](moxfield.com)
- [mtggoldfish.com](mtggoldfish.com)
- [mtgjson.com](mtgjson.com)
- [scryfall.com](scryfall.com)
- [tappedout.net](tappedout.net)
- [tcgplayer.com](tcgplayer.com)


## Known issues

Parsing decklists on some websites require a bit more work:

- Moxfield.com requires a custom User-Agent ([see here](#parsing-from-moxfieldcom))


## Usage


### QuickStart

Start by importing the `mtg_parser` module:

```python
import mtg_parser
```

Now let's parse a decklist (in any of the supported formats) and display the cards:

```python
cards = mtg_parser.parse_deck(url)
for card in cards:
    print(card)
```

`parse_deck()` methods return a generator of `Card` objects matching the following description

```python
class Card:
    name: str
    quantity: int = 1
    extension: Optional[str] = None
    number: Optional[str] = None
    tags: List[str] = []
```


### Advanced - Parsing

`mtg_parser.parse_deck()` is a shortcut method to the specialized versions.
If `url` is a valid Moxfield url, the following lines are equivalent:

```python
cards = mtg_parser.parse_deck(url)
# is the same as:
cards = mtg_parser.moxfield.parse_deck(url)
```

In general, it's advised to use `mtg_parser.parse_deck()` as the overhead is insignificant.


### Advanced - Configuration

> [!NOTE]
> As of `mtg_parser="=>0.0.1a40"` switched to [httpx](https://pypi.org/project/httpx)
> instead of [requests](https://pypi.org/project/requests).

If for any reason, you need to configure how `mtg_parser` fetches remote decklists, you can provide an optional `httpx.Client` object.

```python
import httpx

headers = {'user-agent': 'my-custom-user-agent/0.0.1'}
with httpx.Client(headers=headers) as client:
    cards = mtg_parser.parse_deck(url, http_client=client)
    for card in cards:
        print(card)
```

If no `httpx.Client` object is provided, one will be created for you.


### Parsing MTGO / MTGA

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

cards = mtg_parser.parse_deck(deck_list)
# or the less recommended form:
# cards = mtg_parser.decklist.parse_deck(deck_list)
for card in cards:
    print(card)
```

### Parsing from aetherhub.com

`mtg_parser` can parse public decks from [aetherhub.com](aetherhub.com)

```python
import mtg_parser

url = 'https://aetherhub.com/Deck/<deck_name>'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.aetherhub.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from archidekt.com

`mtg_parser` can parse public decks from [archidekt.com](archidekt.com)

```python
import mtg_parser

url = 'https://www.archidekt.com/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.archidekt.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from deckstats.net

`mtg_parser` can parse public decks from [deckstats.net](deckstats.net)

```python
import mtg_parser

url = 'https://deckstats.net/decks/<user_id>/<deck_id>'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.deckstats.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from moxfield.com

`mtg_parser` can parse public decks from [moxfield.com](moxfield.com)


> [!IMPORTANT]
> Moxfield.com prohibits scraping their website, as it violates their Terms of Service.
>
> For authorized access, please contact support@moxfield.com to request a custom User-Agent.


```python
import httpx
import mtg_parser

url = 'https://www.moxfield.com/decks/<deck_id>'

headers = {'user-agent': '<MOXFIELD_USER_AGENT>'}
with httpx.Client(headers=headers) as client:
    cards = mtg_parser.parse_deck(url, http_client=client)
    # or the less recommended form:
    # cards = mtg_parser.moxfield.parse_deck(url, http_client=client)
for card in cards:
    print(card)
```


### Parsing from mtggoldfish.com

`mtg_parser` can parse public decks from [mtggoldfish.com](mtggoldfish.com)

```python
import mtg_parser

url = 'https://www.mtggoldfish.com/deck/<deck_id>'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.mtggoldfish.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from mtgjson.com

`mtg_parser` can parse decks from [mtgjson.com](mtgjson.com)

```python
import mtg_parser

url = 'https://mtgjson.com/api/v5/decks/<deck_name>.json'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.mtgjson.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from scryfall.com

`mtg_parser` can parse public decks from [scryfall.com](scryfall.com)

```python
import mtg_parser

url = 'https://scryfall.com/<userid>/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.scryfall.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from tappedout.net

`mtg_parser` can parse public decks from [tappedout.net](tappedout.net)

```python
import mtg_parser

url = 'https://tappedout.net/mtg-decks/<deck_id>/'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.tappedout.parse_deck(url)
for card in cards:
    print(card)
```


### Parsing from tcgplayer.com

`mtg_parser` can parse public decks from [tcgplayer.com](tcgplayer.com)

```python
import mtg_parser

url = 'https://www.tcgplayer.com/content/magic-the-gathering/deck/<deck_name>/<deck_id>'
# or url = 'https://infinite.tcgplayer.com/magic-the-gathering/deck/<deck_name>/<deck_id>'

cards = mtg_parser.parse_deck(url)
# or the less recommended form:
# cards = mtg_parser.tcgplayer.parse_deck(url)
for card in cards:
    print(card)
```
