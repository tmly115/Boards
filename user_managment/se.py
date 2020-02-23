# Simple Encryption, used to encrypt and decrypt the user names with the password as a key.

def generate_key(string):
	key = []
	for char in list(string):
		key.append(ord(char))
	return key



def encrypt_char(key, char):
	en_char = ord(char)
	for x in key:
		en_char = en_char + x
	return chr(en_char)

def encrypt_line(key, line):
	en_line = ''
	for char in list(line):
		en_line = en_line + encrypt_char(key, char)
	return en_line




def decrypt_char(key, char):
	de_char = ord(char)
	for x in key:
		de_char = de_char - x
	return chr(de_char)

def decrypt_line(key, line):
	de_line = ''
	for char in list(line):
		de_line = de_line + decrypt_char(key, char)
	return de_line
