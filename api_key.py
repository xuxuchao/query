#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
------------------------------------
# @FileName    :api_keys.py
# @Time        :2021/8/28 10:25
# @Author      :xieyuanzuo
# @description :
------------------------------------
"""

import json
from Crypto.Cipher import AES
from base64 import b64decode, b64encode
import time

BLOCK_SIZE = AES.block_size
# 不足BLOCK_SIZE的补位(s可能是含中文，而中文字符utf-8编码占3个位置,gbk是2，所以需要以len(s.encode())，而不是len(s)计算补码)
pad = lambda s: s + (BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s.encode()) % BLOCK_SIZE)
# 去除补位
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class AESCipher:
    def __init__(self, key: str):
        self.key = key  # 密钥
        self.iv = key[0:16]  # 偏移量

    def encrypt(self, text):
        """
        加密 ：先补位，再AES加密，后base64编码
        :param text: 需加密的明文
        :return:
        """
        # text = pad(text) 包pycrypto的写法，加密函数可以接受str也可以接受bytess
        text = pad(text).encode()  # 包pycryptodome 的加密函数不接受str
        cipher = AES.new(key=self.key.encode(), mode=AES.MODE_CBC, IV=self.iv.encode())
        encrypted_text = cipher.encrypt(text)
        # 进行64位的编码,返回得到加密后的bytes，decode成字符串
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        """
        解密 ：偏移量为key[0:16]；先base64解，再AES解密，后取消补位
        :param encrypted_text : 已经加密的密文
        :return:
        """
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key.encode(), mode=AES.AESMode, IV=self.iv.encode())
        decrypted_text = cipher.decrypt(encrypted_text)
        return unpad(decrypted_text).decode('utf-8')


def timestamp_to_str(timestamp=None, format='%Y-%m-%d %H:%M:%S'):
    if timestamp:
        time_tuple = time.localtime(timestamp)  # 把时间戳转换成时间元祖
        result = time.strftime(format, time_tuple)  # 把时间元祖转换成格式化好的时间
        return result
    else:
        return time.strptime(format)


def get_apikeys_base(data):
    """
    获取加密后的apikeys,用于base_api的封装
    :param token:
    :param data: data中包含url、headers等请求数据
    :return:
    """
    token = data["headers"]["Authorization"]
    if "params" in data.keys():
        params = data["params"]
        params_format = "?" + "&".join(f"{k}={v}" for k, v in params.items() if v)
        url = data["url"] + params_format
        del data["params"]
        data["url"] = url
    else:
        url = data["url"]
    str_encrypt = {"url": url, "token": token, "timestamp": timestamp_to_str(time.time())}
    apikeys = AESCipher(key=token[-16:]).encrypt(json.dumps(str_encrypt))
    return apikeys, data


def get_apikeys(headers, url, method, params):
    """
    获取加密后的apikeys，用于do_request的封装
    :param token:
    :param headers: 其中包含token信息
    :param params: 当为get请求时，params参数值
    :param url:
    :return:
    """
    token = headers["Authorization"]
    if params and method == "get":
        params_format = "?" + "&".join(f"{k}={v}" for k, v in params.items() if v)
        url = url + params_format
    str_encrypt = {"url": url, "token": token, "timestamp": timestamp_to_str(time.time())}
    apikeys = AESCipher(key=token[-16:]).encrypt(json.dumps(str_encrypt))
    return apikeys


import requests
import urllib3
urllib3.disable_warnings()


def get_token(host, user_id, password):
    url = "https://{host}/opra-api/sys/login"
    login_data = {"userId": user_id, "password": password}
    res = requests.post(url.format(host=host), json=login_data, verify=False)
    if res.status_code == 200:
        token = res.json().get("accessToken")
        return token


if __name__ == '__main__':
    url = "/upl-file/test/encry?data=邹犀撃&type=NAME"
    token = get_token("10.1.19.222", "upl", "Abc@12345")
    str_encrypt = {"url": url, "token": token, "timestamp": timestamp_to_str(time.time())}
    s = AESCipher(key=token[-16:]).encrypt(json.dumps(str_encrypt))
    print("===========Authorization", token)
    print("===========apikey", s)
