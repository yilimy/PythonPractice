# -*- coding:utf-8 -*-

from string import ascii_letters, digits
import random
from Crypto.Cipher import AES
from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64
import binascii
import json
from urllib import request, parse

# 获取 大小写字母 + 数字
_charset = ascii_letters + digits;

def rand_char(num=16):
    # 下划线表示临时变量，只使用一次
    # choice表示选择区间
    return ''.join(random.choice(_charset) for _ in range(num))

def aes_encrypt(msg, key, iv='0102030405060708'):

    def padded(msg):
        pad = 16 - len(msg) % 16
        return msg + pad * chr(pad)

    msg = padded(msg)
    cryptor = AES.new(key, IV=iv, mode=AES.MODE_CBC)
    text = cryptor.encrypt(msg)
    text = base64.b64encode(text)
    return text;

def gen_param(d, i):
    # 对称加密一次
    text = aes_encrypt(d, '0CoJUm6Qyw8W8jud')
    # 对称加密二次
    text = aes_encrypt(text.decode(), i)
    return text;

def rsa_encrypt(msg):
    cryptor = RSA.construct((0x00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7,
                             0x10001))
    text = cryptor.encrypt(msg[::-1], '')[0]
    text = binascii.b2a_hex(text)
    return text

def rsa_encrypt2(msg):
    msg = binascii.b2a_hex(msg[::-1].encode())
    msg = int(msg, 16)
    text = 1
    for _ in range(0x10001):
        text *= msg
        text %= 0x00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
        return format(text, 'x')

def rsaEncrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(text.encode(), 16)**int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)

def encrypt(query):
    query = json.dumps(query)
    rand_i = rand_char(16)
    rand_i = 16 * 'F'
    param = gen_param(query, rand_i)
    # enc_key = rsa_encrypt(rand_i)
    enc_key = '257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c'
    print(enc_key)
    data = {
        'param': param.decode(),
        'encSecKey': enc_key
    }
    return data

def doPost():
    music_id = '456318028'
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(music_id)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com/',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
    query = {
        'rid': 'R_SO_4_{}'.format(music_id),
        'offset': '0',
        'total': 'true',  # 第一页时为true，其他页为false
        'limit': '20',
        'csrf_token': ''  # token 可以为空
    }
    data = parse.urlencode(encrypt(query)).encode()
    req = request.Request(url, headers=headers, data=data)
    response = request.urlopen(req, timeout=15.0)
    print(response.getcode())
    res_data = response.read()
    print(res_data)
    rjson = json.loads(res_data, strict=False)
    for item in rjson['comments']:
        print(item['content'])

def test_rsa():
    text = 16 * 'F'
    print('text type = %s\n %s' % (type(text), text))
    pubKey = '010001'
    modulus = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
    res = rsaEncrypt(text, pubKey, modulus)
    print(res)

if __name__ == '__main__':
    # test_rsa()
    rsa_res = rsa_encrypt(16 * 'F')
    print(rsa_res)
    # doPost()

