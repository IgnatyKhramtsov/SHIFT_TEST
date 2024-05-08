from argon2 import PasswordHasher


ph = PasswordHasher()


def get_password_hash(password):
    return ph.hash(password)


def verify_password(plain_password, hashed_password):
    return ph.verify(hashed_password, plain_password)

