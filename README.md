# Quickstart

	make install
	make test
	make build
	make clean

or

	make

# Publish a new version

## Test

	poetry version (premajor|preminor|prepatch|prerelease)
	make test
	make lint
	make build
	make test-publish

## Publish

	poetry version (major|minor|patch)
	make build
	make publish
