# -*- coding=utf-8 -*-

# 对称加密AES
# pad: ZeroPadding
# mode: cbc

from Crypto.Cipher import AES
from string import ascii_letters, digits
import base64
import random

class prprcrypt():
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv
        self.mode = AES.MODE_CBC

    def encrypto(self, text):
        cryptor = AES.new(self.key, mode = self.mode, IV = self.iv)
        # 被加密的明文需要是16的倍数
        # 做补码
        length = 16
        # 对中文 (如果含有) 进行utf-8编码后再测量长度
        count = len(text.encode('utf-8'))
        add = length - (count % length)
        if add != 0:
            text = text + add * '\0'
        print('text = %s, and length = %d, count = %d .' % (text, len(text), count))
        cipher_text = cryptor.encrypt(text)
        print('cipher_text = %s ' % cipher_text)
        return base64.b64encode(cipher_text)

    def decrypt(self, text):
        cryptor = AES.new(self.key, mode=self.mode, IV=self.iv)
        str_64 = base64.b64decode(text);
        print('str 64 = %s ' % str_64)
        plain_text = cryptor.decrypt(str_64)
        print('plain_text = %s ' % plain_text)
        # 返回的结果需要对 bytes 去零处理
        return plain_text.rstrip(b'\0')

def random_num(num):
    _charset = ascii_letters + digits
    return ''.join(random.choice(_charset) for _ in range(num))

if __name__ == '__main__':
    # AES key must be either 16, 24, or 32 bytes long
    key = random_num(16)
    print('key = %s, and length = %d .' % (key, len(key)))
    # IV must be 16 bytes long
    secret = random_num(16)
    print('secret = %s, and length = %d .' % (secret, len(secret)))
    prpr = prprcrypt(key, secret)
    e = prpr.encrypto('im cipher no pl中文')
    print('encrypt result = %s' % e)
    d = prpr.decrypt(e)
    print(d.decode())

