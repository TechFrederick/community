import base64
import hashlib


def generate_id(old_id: str | int, salt: str) -> str:
    """Generate a short ID.

    A salt is expected to prevent collisions between different sources
    of IDs. For instance, if two fetching sources get data that use integer IDs,
    it would be very easy to get ID collisions.
    """
    salted_id = str(old_id) + salt
    hash_object = hashlib.sha256()
    hash_object.update(salted_id.encode("utf-8"))
    hex_digest = hash_object.digest()
    encoded_hash = base64.urlsafe_b64encode(hex_digest)
    safe_hash = (
        encoded_hash.decode("utf-8").rstrip("=").replace("-", "").replace("_", "")
    )
    return safe_hash[:8]
