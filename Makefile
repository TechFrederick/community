build:
	@venv/bin/python build.py

serve:
	venv/bin/python -m http.server --directory out

bootstrap:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
