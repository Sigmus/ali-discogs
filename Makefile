.PHONY: install fetch match match-offline build serve test

UV ?= uv
HOST ?= 127.0.0.1
PORT ?= 8000

install:
	$(UV) sync

fetch: install
	$(UV) run ali-discogs fetch

match: install
	$(UV) run ali-discogs match

match-offline: install
	$(UV) run ali-discogs match --offline

build:
	rm -rf dist
	mkdir -p dist/data
	cp explorer/index.html explorer/app.js explorer/style.css dist/
	cp explorer/data/fixture.json dist/data/
	cp data/collection_matches.json data/summary.json dist/data/
	cp data/qobuz_matches.json dist/data/
	touch dist/.nojekyll

serve: build
	cd dist && python3 -m http.server $(PORT) --bind $(HOST)

test: install
	$(UV) run python -m unittest discover -s tests -v
	node explorer/test/normalize.test.js
	$(UV) run --with 'requests>=2.32,<3' python -m unittest discover -s scripts/test -v
	$(UV) run python scripts/spotify_followup_verify.py
