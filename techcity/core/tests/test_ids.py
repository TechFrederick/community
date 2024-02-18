from techcity.core.ids import generate_id


def test_generates_id():
    """An 8 character ID is created from an input ID."""
    old_id = "1234567890abcdef"
    salt = "meetup"

    new_id = generate_id(old_id, salt)

    assert len(new_id) == 8
    assert new_id == "IR8XK73o"
