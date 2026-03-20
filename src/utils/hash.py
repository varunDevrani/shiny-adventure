from argon2 import PasswordHasher
from argon2.exceptions import Argon2Error


passwordHasher = PasswordHasher()



def hash_password(plain_passwd: str) -> str:
	return passwordHasher.hash(plain_passwd)


def verify_password(hash_passwd: str, plain_passwd: str) -> bool:
	try:
		passwordHasher.verify(hash_passwd, plain_passwd)
		return True
	except Argon2Error:
		return False

