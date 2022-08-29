# How to contribute to mtg-parser


## Getting started

This project uses `poetry`, please refer to [their website](https://python-poetry.org) on how to install it.

Then, clone the repository and run:

	$ make install


## Run tests

For fast iteration, run:

	$ make test

For a full checkup (including slow tests):

	$ make test-all


## Run linters

For fast iteration, run:

	$ make lint

For a full checkup:

	$ make lint-all


## How to publish a new version

### Test version

	$ poetry version (premajor|preminor|prepatch|prerelease)
	$ make release
	$ make test-publish

### Release version

	$ poetry version (major|minor|patch)
	$ make release
	$ make publish
