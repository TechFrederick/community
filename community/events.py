import os

import requests
from dotenv import load_dotenv


def fetch():
    load_dotenv()
    print("Fetching events...")
    session = requests.Session()
    login(session)

    response = session.get("https://www.meetup.com/python-frederick/events/rss/")
    print(response.status_code)
    print(response.content.decode())


def login(session):
    """Do the login dance needed to get a valid authenticated session."""
    request_body = {
        "operationName": "login",
        "variables": {
            "input": {
                "email": os.environ["MEETUP_EMAIL"],
                "password": os.environ["MEETUP_PASSWORD"],
                "rememberMe": False,
            }
        },
        # Without this section, things break for reasons that I don't understand.
        # The Apollo docs seem to indicate that this is for persisting long query strings,
        # but the login request is done with a POST. *shrug*
        # I don't know how long Meetup will consider this a valid SHA.
        # I found this by inspecting the login payload.
        "extensions": {
            "persistedQuery": {
                "version": 1,
                "sha256Hash": "27c2dcd3fe18741b545abf6918eb37aee203463028503aa8b2b959dc1c7aa007",
            }
        },
    }
    # This first request was required before login would work. It's probably setting
    # some initial cookies that must be present.
    response = session.get("https://www.meetup.com")
    response.raise_for_status()

    response = session.post("https://www.meetup.com/gql", json=request_body)
    data = response.json()
    if data["data"]["login"]["error"]:
        raise Exception("failed to login")
