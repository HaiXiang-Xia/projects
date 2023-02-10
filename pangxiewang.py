'''
https://www.pxb7.com/
交易平台数据逆向
数据加密模式:AES-CBC模式
'''

import requests
import time
from fake_useragent import UserAgent
import random
import hashlib
import json
import base64
from Crypto.Cipher import AES
import ast


#AES加密位数补齐
def data_16(x):
    while len(x) % 16 != 0:
        x += '\0'
    return x

#AES解密，CBC模式
def AES_CBC(x):
    k = 'C01F8012D3F6386C'
    v = '245C3EA487E944FD'
    x = data_16(x)
    x = base64.decodebytes(x.encode('utf-8'))
    aes = AES.new(k.encode('utf-8'),AES.MODE_CBC,v.encode('utf-8'))
    date = aes.decrypt(x)
    #匿名函数 : 将AES加解密数据需要16的倍数位，不足需补齐，函数的作用就是将加解密 补齐的添加数据去除，补几位就去除几位
    func = lambda s : s[0: -s[-1]]
    return func(date).decode('utf-8')


#Md5加密
def Hashlib_Md5(x):
    Md5 = hashlib.md5()
    Md5.update(x.encode(encoding='utf-8'))
    md5_x = Md5.hexdigest()
    return md5_x


#请求头 加密参数  token,ApiToken
def head():
    a = ''
    i = 0
    while i < int(10 * random.random()) + 1:
        i += 1
        a = a + str(int(10 * random.random()))
    token = Hashlib_Md5(a)
    new_time = time.strftime('%Y-%m-%d',time.localtime()).split('-')
    year = new_time[0]
    month = '02' if int(new_time[1]) < 10 else str(int(new_time[1]))
    apitoken = year + month + 'PXB7' + token
    Apitoken = Hashlib_Md5(apitoken)
    return token,Apitoken

#处理数据
def display(date):
    dict_1 = {}
    for i in date["list"]:
        try:
            dict_1["大区"] = i["category"][0]["value"]
            dict_1["服务器"] = i["category"][1]["value"]
        except:
            pass
        dict_1["价格"] = i["price"]
        dict_1["热度"] = i["click"]
        dict_1["详细信息"] = i["name"]
        dict_1["图片"] = i["image"].replace('\\','')
        print(dict_1)

#请求网址
def display_url(url):
    token,ApiToken = head()
    headers = {
        'ApiToken': ApiToken,
        'Accept': "application/json, text/plain, */*",
        'LoginStatus': 'false',
        'Host': 'api.pxb7.com',
        'Origin': 'https://www.pxb7.com',
        'token': token,
        'User-Agent': UserAgent().random
    }
    respose = requests.get(url=url,headers=headers).json()['data']
    date = AES_CBC(respose)
    try:
        content = ast.literal_eval(date)
    except:
        content = json.loads(date)
    return content


def main():
    game_url = 'https://api.pxb7.com/api/product/list?game_id=15&rec=&category={"1":0,"9":0,"10":[],"11":[],"12":[],"13":[],"14":[],"15":[],"17":0}&scope={"min_price":"","max_price":""}&sort={"type":"","method":2}&page=2'
    game_date = display_url(game_url)
    display(game_date)


if __name__ == '__main__':
    main()
