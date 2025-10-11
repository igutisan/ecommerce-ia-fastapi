from argon2 import PasswordHasher


ph = PasswordHasher()


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except:
        return False
