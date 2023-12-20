build:
	@venv/bin/python build.py

bootstrap:
	test -d venv || python3 -m venv venv
	venv/bin/pip install -r requirements.txt
