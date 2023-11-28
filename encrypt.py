#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
import base64
 
from Crypto import Random
from Crypto.Cipher import AES
 
BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]
 
class AESCipher:
 
    def __init__(self, key):
        self.key = "{: <32}".format(key).encode("utf-8")
 
    def encrypt(self, raw):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        print("dir",dir(cipher))
        # return base64.b64encode(cipher.encrypt(raw) + bytes("::", "utf-8") + iv).decode("ascii")
 
    def decrypt(self, enc):
        (enc, iv) = base64.b64decode(enc).split(bytes("::", "utf-8"))
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc).decode("ascii"))
    
if __name__ == "__main__": 
    cipher = AESCipher('mysecretpassword@')
    encrypted = cipher.encrypt('Secret Message A')
    # decrypted = cipher.decrypt(encrypted)
    # print (encrypted)
    # print (decrypted)