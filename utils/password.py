from argon2 import PasswordHasher


def password_match(pass1: str, pass2: str):
    return pass1 == pass2


def hash_password(user_password: str):
    pw_object = PasswordHasher()
    hashed_pass = pw_object.hash(password=user_password)
    return hashed_pass


def password_match(password_input: str, hash: str):
    pw_object = PasswordHasher()
    return pw_object.verify(hash=hash, password=password_input)
