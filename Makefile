.PHONY: frontend

run:
	@uv run honcho start

bootstrap:
	@bin/bootstrap

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

build:
	docker compose build

shell:
	docker compose run --rm web bash

django_shell:
	uv run manage.py shell_plus
