# mtg-parser


## How to install

	pip install mtg-parser


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
