run:
	venv/bin/honcho start

build:
	@venv/bin/python -m community

watcher:
	venv/bin/watchmedo shell-command \
		--pattern='*.py;*.html' \
		--recursive \
		--command='make build' \
		--drop \
		community templates

serve:
	venv/bin/python -m http.server --directory out 8000

bootstrap:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
	npm install
