run:
	venv/bin/honcho start

build:
	@venv/bin/python community/build.py

watcher:
	venv/bin/watchmedo shell-command \
		--pattern='*.py;*.html' \
		--recursive \
		--command='make build' \
		--drop \
		community templates

serve:
	venv/bin/python -m http.server --directory out

bootstrap:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
