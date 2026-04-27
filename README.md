# mtg-parser

![PyPI](https://img.shields.io/pypi/v/mtg-parser)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mtg-parser)
![Github - Latest Release](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/latest_release.yaml?label=Release%20tests)
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
- [aetherhub.com](#parsing-from-aetherhubcom)
- [archidekt.com](#parsing-from-archidektcom)
- [deckstats.net](#parsing-from-deckstatsnet)
- [moxfield.com](#parsing-from-moxfieldcom)
- [mtggoldfish.com](#parsing-from-mtggoldfishcom)
- [mtgjson.com](#parsing-from-mtgjsoncom)
- [mtgvault.com](#parsing-from-mtgvaultcom)
- [scryfall.com](#parsing-from-scryfallcom)
- [tappedout.net](#parsing-from-tappedoutnet)
- [tcgplayer.com](#parsing-from-tcgplayercom)


## Known issues

Parsing decklists on some websites require specific configuration.

- The following websites require a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`:
  - [aetherhub.com](#parsing-from-aetherhubcom)
  - [deckstats.net](#parsing-from-deckstatsnet)
  - [mtggoldfish.com](#parsing-from-mtggoldfishcom)
  - [mtgvault.com](#parsing-from-mtgvaultcom)
- [moxfield.com](#parsing-from-moxfieldcom) requires a custom User-Agent ([see here](#parsing-from-moxfieldcom))


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

For conveniency, `mtg_parser` provides an optional `HttpClientFacade` to facilitate handling of different websites with different http clients.


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

![Aetherhub Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_aetherhub.yaml?label=Aetherhub%20integration%20tests)

`mtg_parser` can parse public decks from [aetherhub.com](https://aetherhub.com)

> [!IMPORTANT]
> aetherhub.com requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`.


```python
import cloudscraper
import mtg_parser

url = 'https://aetherhub.com/Deck/<deck_name>'

cards = mtg_parser.parse_deck(url, cloudscraper.create_scraper())
```


### Parsing from archidekt.com

![Archideckt Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_archidekt.yaml?label=Archideckt%20integration%20tests)

`mtg_parser` can parse public decks from [archidekt.com](https://archidekt.com)

```python
import requests
import mtg_parser

url = 'https://www.archidekt.com/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from deckstats.net

![Deckstats Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_deckstats.yaml?label=Deckstats%20integration%20tests)

`mtg_parser` can parse public decks from [deckstats.net](https://deckstats.net)

> [!IMPORTANT]
> deckstats.net requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`.


```python
import cloudscraper
import mtg_parser

url = 'https://deckstats.net/decks/<user_id>/<deck_id>'

cards = mtg_parser.parse_deck(url, cloudscraper.create_scraper())
```


### Parsing from moxfield.com

![Moxfield Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_moxfield.yaml?label=Moxfield%20integration%20tests)

`mtg_parser` can parse public decks from [moxfield.com](https://moxfield.com)


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

![MTGGoldfish Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_mtggoldfish.yaml?label=MTGGoldfish%20integration%20tests)

`mtg_parser` can parse public decks from [mtggoldfish.com](https://mtggoldfish.com)

> [!IMPORTANT]
> mtggoldfish.com requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`.


```python
import cloudscraper
import mtg_parser

url = 'https://www.mtggoldfish.com/deck/<deck_id>'

cards = mtg_parser.parse_deck(url, cloudscraper.create_scraper())
```


### Parsing from mtgjson.com

![mtgjson Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_mtgjson.yaml?label=mtgjson%20integration%20tests)

`mtg_parser` can parse decks from [mtgjson.com](https://mtgjson.com)

```python
import requests
import mtg_parser

url = 'https://mtgjson.com/api/v5/decks/<deck_name>.json'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from mtgvault.com

![MTGVault Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_mtgvault.yaml?label=mtgvault%20integration%20tests)

`mtg_parser` can parse public decks from [mtgvault.com](https://www.mtgvault.com)

> [!IMPORTANT]
> mtgvault.com requires a Cloudflare-bypass `requests` compatible http client such as `cloudscraper`.

```python
import cloudscraper
import mtg_parser

url = 'https://www.mtgvault.com/<username>/decks/<deck_name>/'

cards = mtg_parser.parse_deck(url, cloudscraper.create_scraper())
```


### Parsing from scryfall.com

![Scryfall Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_scryfall.yaml?label=Scryfall%20integration%20tests)

`mtg_parser` can parse public decks from [scryfall.com](https://scryfall.com)

```python
import requests
import mtg_parser

url = 'https://scryfall.com/<userid>/decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from tappedout.net

![Tappedout Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_tappedout.yaml?label=Tappedout%20integration%20tests)

`mtg_parser` can parse public decks from [tappedout.net](https://tappedout.net)

```python
import requests
import mtg_parser

url = 'https://tappedout.net/mtg-decks/<deck_id>/'

cards = mtg_parser.parse_deck(url, requests.Session())
```


### Parsing from tcgplayer.com

![TCGplayer Integration Tests](https://img.shields.io/github/actions/workflow/status/lheyberger/mtg-parser/integration_tcgplayer.yaml?label=TCGplayer%20integration%20tests)

`mtg_parser` can parse public decks from either [tcgplayer.com](https://www.tcgplayer.com) or [infinite.tcgplayer.com](https://infinite.tcgplayer.com)

```python
import requests
import mtg_parser

url = 'https://www.tcgplayer.com/content/magic-the-gathering/deck/<deck_name>/<deck_id>'
# or url = 'https://infinite.tcgplayer.com/magic-the-gathering/deck/<deck_name>/<deck_id>'

cards = mtg_parser.parse_deck(url, requests.Session())
```
