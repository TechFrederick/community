.PHONY: frontend

run:
	@uv run honcho start

bootstrap:
	uv sync
	npm --prefix frontend install

serve:
	uv run manage.py runserver

frontend:
	npm --prefix frontend run tailwind

fetch:
	@uv run manage.py fetch_events

# This is mostly for the scenario where the output data files need to be manipulated
# and reformatted and we don't want to keep hitting the Meetup APIs slowly.
fetch-cached:
	@uv run manage.py fetch_events --cached

test:
	uv run pytest --cov techcity

# Test with migrations to make sure they work.
ci:
	uv run pytest --cov techcity --migrations

# Build the static site
build:
	@uv run manage.py distill-local out --force --collectstatic

# Serve the static site locally
serve-static:
	@uv run python -m http.server --directory out

