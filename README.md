# mtg-parser

## How to install

	pip install mtg-parser

## Run tests

This project uses `poetry`, please refer to [their website](https://python-poetry.org) on how to install it.

Then, clone the repository and:

	$ make install lint test

## How to publish a new version

### Test version

	$ poetry version (premajor|preminor|prepatch|prerelease)
	$ make test lint build clean test-publish

### Release version

	$ poetry version (major|minor|patch)
	$ make test lint build clean publish

## How to use

	import mtg_parser
	
	decklist = """
		1 Atraxa, Praetors' Voice
		1 Imperial Seal
		1 Lim-Dûl's Vault
		1 Jeweled Lotus (CMR) 319
		1 Llanowar Elves (M12) 182
		3 Brainstorm #Card Advantage #Draw
	"""
	
	cards = mtg_parser.parse_deck(decklist)
	
	for card in cards:
		print(card['quantity'], card['card_name'])
