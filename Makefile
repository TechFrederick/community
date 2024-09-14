.PHONY = build

run:
	@uv run honcho start

bootstrap:
	uv sync
	npm --prefix techcity/services/builder install

build:
	@uv run techcity build

watcher:
	uv run watchmedo shell-command \
		--pattern='*.html;*.md;*.py;*.yaml' \
		--recursive \
		--command='make build' \
		--drop \
		techcity data

serve:
	uv run manage.py runserver

frontend:
	npm --prefix techcity/services/builder run tailwind

fetch:
	@uv run techcity fetch

# This is mostly for the scenario where the output data files need to be manipulated
# and reformatted and we don't want to keep hitting the Meetup APIs slowly.
fetch-cached:
	@uv run techcity fetch --cached

check:
	uv run scrapy crawl --overwrite-output checker.jsonl --nolog crawler

test-ci: test
	uv run honcho -f checker/Procfile.checker start
	cat checker.jsonl
	test ! -s checker.jsonl

test:
	uv run pytest --cov techcity
