#define PY_SSIZE_T_CLEAN
#include <Python.h>

from Crypto.Cipher import AES
import hashlib

def pad(data):
    length = 16 - (len(data) % 16)
    data += chr(length) * length
    return data

def encrypt(plainText, workingKey):
    iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    plainText = pad(plainText)
    encDigest = hashlib.md5()
    encDigest.update(workingKey.encode('utf-8'))
    enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv.encode('utf-8'))
    encryptedText = enc_cipher.encrypt(plainText.encode('utf-8')).hex()
    return encryptedText

def decrypt(cipherText, workingKey):
    iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    decDigest = hashlib.md5()
    decDigest.update(workingKey.encode('utf-8'))
    encryptedText = bytes.fromhex(cipherText)
    dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv.encode('utf-8'))
    decryptedText = dec_cipher.decrypt(encryptedText)
    return decryptedText.decode('utf-8').rstrip('\0')






# from Crypto.Cipher import AES
# import md5

# def pad(data):
# 	length = 16 - (len(data) % 16)
# 	data += chr(length)*length
# 	return data

# def encrypt(plainText,workingKey):
# 	iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
# 	plainText = pad(plainText)
# 	encDigest = md5.new ()
# 	encDigest.update(workingKey)
# 	enc_cipher = AES.new(encDigest.digest(), AES.MODE_CBC, iv)
# 	encryptedText = enc_cipher.encrypt(plainText).encode('hex')
# 	return encryptedText



# def decrypt(cipherText,workingKey):
#     iv = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
#     decDigest = md5.new ()
#     decDigest.update(workingKey)
#     encryptedText = cipherText.decode('hex')
#     dec_cipher = AES.new(decDigest.digest(), AES.MODE_CBC, iv)
#     decryptedText = dec_cipher.decrypt(encryptedText)
#     return decryptedText
