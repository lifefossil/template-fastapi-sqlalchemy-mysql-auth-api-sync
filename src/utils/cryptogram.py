from passlib.handlers.pbkdf2 import pbkdf2_sha256


def encode_password(password: str):
    return pbkdf2_sha256.hash(password)


def check_password(plain_password, encoded_password):
    return pbkdf2_sha256.verify(plain_password, encoded_password)
