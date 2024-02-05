run:
	venv/bin/honcho start

bootstrap:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
	npm install

build:
	@venv/bin/techcity build

watcher:
	venv/bin/watchmedo shell-command \
		--pattern='*.html;*.md;*.py' \
		--recursive \
		--command='make build' \
		--drop \
		techcity data templates

serve:
	venv/bin/python -m http.server --directory out 8000

fetch:
	@venv/bin/techcity fetch

# This is mostly for the scenario where the output data files need to be manipulated
# and reformatted and we don't want to keep hitting the Meetup APIs slowly.
fetch-cached:
	@venv/bin/techcity fetch --cached

check:
	venv/bin/scrapy crawl --overwrite-output checker.jsonl --nolog crawler

test-ci:
	honcho -f Procfile.checker start
	cat checker.jsonl
	test ! -s checker.jsonl
