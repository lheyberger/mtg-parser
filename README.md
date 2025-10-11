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
- `python>=3.9`

To install `mtg_parser`, simply run one of the following commands in the terminal of your choice:

```shell
$ pip install mtg-parser
# or
$ uv add mtg-parser
# or
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

Parsing decklists on some websites require specific configuration:

- [aetherhub.com](aetherhub.com) requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`
- [moxfield.com](moxfield.com) requires a custom User-Agent ([see here](#parsing-from-moxfieldcom))


## Usage


### QuickStart

> [!NOTE]
> As of `mtg_parser="=>0.0.1a50"` doesn't provide a default http client anymore.


To parse a decklist with `mtg_parser`, you need to provide an HTTP client that implements a `requests` compatible interface (such as `requests` or `httpx`).


```python
import requests
import mtg_parser

cards = mtg_parser.parse_deck(url, requests.Session())
```

For conveniency, `mtg_parser` provides an optional HttpClientFacade to facilitate handling of different websites with different http clients.


```python
import cloudscraper
import httpx
import mtg_parser

client_facade = mtg_parser.HttpClientFacade(httpx.Client(timeout=10.0))
client_facade.set_override('aetherhub.com', cloudscraper.create_scraper())
client_facade.set_override('moxfield.com', httpx.Client(
    timeout=10.0,
    headers={'User-Agent': os.getenv('MOXFIELD_USER_AGENT')},
))

cards = mtg_parser.parse_deck(url, client_facade)
```


### Return format

`parse_deck()` returns an `Iterable[Card]` matching the following description

```python
class Card:
    name: str
    quantity: int
    extension: Optional[str]
    number: Optional[str]
    tags: Iterable[str] = []

cards = mtg_parser.parse_deck(url, http_client)
for card in cards:
    print(card)
```


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
```

### Parsing from aetherhub.com

`mtg_parser` can parse public decks from [aetherhub.com](aetherhub.com)

> [!IMPORTANT]
> aetherhub.com requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`.


```python
import cloudscraper
import mtg_parser

url = 'https://aetherhub.com/Deck/<deck_name>'

cards = mtg_parser.parse_deck(url, cloudscraper.create_scraper())
```


### Parsing from archidekt.com

`mtg_parser` can parse public decks from [archidekt.com](archidekt.com)

```python
import requests
import mtg_parser

url = 'https://www.archidekt.com/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from deckstats.net

`mtg_parser` can parse public decks from [deckstats.net](deckstats.net)

```python
import requests
import mtg_parser

url = 'https://deckstats.net/decks/<user_id>/<deck_id>'

cards = mtg_parser.parse_deck(url, requests.Session())
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
with httpx.Client(headers=headers) as http_client:
    cards = mtg_parser.parse_deck(url, http_client)
```


### Parsing from mtggoldfish.com

`mtg_parser` can parse public decks from [mtggoldfish.com](mtggoldfish.com)

```python
import requests
import mtg_parser

url = 'https://www.mtggoldfish.com/deck/<deck_id>'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from mtgjson.com

`mtg_parser` can parse decks from [mtgjson.com](mtgjson.com)

```python
import requests
import mtg_parser

url = 'https://mtgjson.com/api/v5/decks/<deck_name>.json'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from scryfall.com

`mtg_parser` can parse public decks from [scryfall.com](scryfall.com)

```python
import requests
import mtg_parser

url = 'https://scryfall.com/<userid>/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from tappedout.net

`mtg_parser` can parse public decks from [tappedout.net](tappedout.net)

```python
import requests
import mtg_parser

url = 'https://tappedout.net/mtg-decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from tcgplayer.com

`mtg_parser` can parse public decks from either [tcgplayer.com](tcgplayer.com) or [infinite.tcgplayer.com](infinite.tcgplayer.com)

```python
import requests
import mtg_parser

url = 'https://www.tcgplayer.com/content/magic-the-gathering/deck/<deck_name>/<deck_id>'
# or url = 'https://infinite.tcgplayer.com/magic-the-gathering/deck/<deck_name>/<deck_id>'

cards = mtg_parser.parse_deck(url, requests.Session())
```
