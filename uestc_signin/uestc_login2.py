import requests
import re
import Crypto.Random
from Crypto.Cipher import AES
import hashlib
import binascii
from io import StringIO
from Crypto.Cipher import AES
import math
import random
from hashlib import md5
import base64
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def _rds(l):
    _chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678'
    _chars_len = len(_chars)
    retStr = ''
    for i in range(l):
        retStr += _chars[math.floor(random.random() * _chars_len)]
    return retStr


class AESCipher:
    def __init__(self, key):
        self.key = key.encode('utf-8')

    def encrypt(self, data):
        vector = _rds(16).encode('utf-8')
        encryption_cipher = AES.new(self.key, AES.MODE_CBC, vector)
        return encryption_cipher.encrypt(pad(data,  AES.block_size))

    def decrypt(self, data):
        data = base64.b64decode(data)
        file_vector = _rds(16).encode('utf-8')
        decryption_cipher = AES.new(self.key, AES.MODE_CBC, file_vector)
        return unpad(decryption_cipher.decrypt(data), AES.block_size)


def encryptAES(data, key):
    data = data.encode('utf-8')
    encrypted = base64.b64encode(AESCipher(key).encrypt(data))
    return encrypted


if __name__ == '__main__':
    # print('TESTING ENCRYPTION')
    # msg = (_rds(64)+"hello").encode('utf-8')
    # key = "EDQmU7aRvFigFnIV"

    # encrypted = base64.b64encode(AESCipher(key).encrypt(msg))
    # print("ddd", encrypted)
    # print('Ciphertext:', encrypted)
    # print(encrypted)
    # print('\nTESTING DECRYPTION')
    # decrypted = AESCipher(key).decrypt(
    #     encrypted).decode('utf-8')

    # print("Original data: ", msg.decode('utf-8'))
    # print("Decripted data:", decrypted)
    # assert msg.decode('utf-8') == decrypted
    # print(base64.b64decode(
    #     "d2p0eZ/yWaVCzX1Km3kR09jCKZRtTCipd/IawZqyRfyyF57MaNjXU/mi64wLW2NyiucWf2focsOII5q4u1bT6BMsrBUhn4w/I8TA8EVPtUI="))
    # data = "hSPxByYkI8PeRaFYzSUU8OclHdhaswsFn/ZD5uljKrZwzDWSF3q2M+COTUnYJho6Snx9oMDrG0B0ZTyTlx7FUVzqyM2cx4oZ2zlpGQ4Qj2c=".encode(
    #     'utf-8')
    # data = "OA/Yi4UAsjB0FhMhjxlb8W6l8zCvy3a063AMPXQDme+P3IdBDgDpgWxmL9l6LRlqQJjUYINm/vDRhpdrXRgQURQ3iqcKpSDemRfoyhFc884="
    # print(AESCipher(key).decrypt(data).decode('utf-8'))

    session = requests.session()
    res = session.get(
        "https://eportal.uestc.edu.cn/login?service=http://eportal.uestc.edu.cn/new/index.html")
    print(res.text)
    salt = re.search(r'pwdDefaultEncryptSalt= \"(.*?)\";',
                     res.text).groups()
    print(salt)

