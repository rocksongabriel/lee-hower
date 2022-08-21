from passlib.context import CryptContext


ctx = CryptContext(schemes=["sha256_crypt", "md5_crypt", "des_crypt"])


def hash_password(raw_password: str) -> str:
    """Return the hashed formed of the raw_password"""
    return ctx.hash(raw_password)


def verify_password(raw_password: str, hashed_password: str) -> bool:
    """
    Return true if the raw_password and hashed_password are equal
    return False otherwise
    """

    # TODO handle the possible error that might occur if the
    # client doesn't pass a valid hash

    return ctx.verify(raw_password, hashed_password)
