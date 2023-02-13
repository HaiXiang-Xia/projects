'''
bilibili数据采集
up主的所有信息
用户ID,用户名 等级 会员(bool值) 简介 关注数 粉丝数 


建议使用 UID查询(UID具有唯一性)
用户名查询可能不准确


会自动新建一个用户文件夹
信息.json     --> 存放用户信息
config.json  --> 存放的是下载过视频信息
video文件     --> 视频文件
'''

import requests
import Download_Video
from fake_useragent import UserAgent
import time
import execjs
import os
import json
import re

#视频
def video(mid,video_path,page):
    wts = int(time.time())
    w_rid = execjs.compile(open('./e.js','r',encoding='utf-8').read()).call('md5',wts)
    headers = {
        'mid': mid,
        'token': '',
        'platform': 'web',
        'w_rid': w_rid,
        'wts': str(wts),
        'origin': 'https://space.bilibili.com',
        'referer': f'https://space.bilibili.com/{mid}',
        'user-agent': UserAgent().random
    }
    page = page
    while 1:
        url = f'https://api.bilibili.com/x/space/wbi/arc/search?mid={mid}&ps=30&tid=0&pn={page}&keyword=&order=pubdate&order_avoided=true&w_rid=e8a8275e2e5aba6a42910c55b4bce9e0&wts={wts}'
        resp = requests.get(url=url,headers=headers).json()
        if not resp["data"]["list"]["vlist"]:
            break
        video_list = []
        r = re.compile(r'[-,$()#+&*]')
        for k in resp["data"]["list"]["vlist"]:
            title = re.sub(r,'',k["title"])
            video_list.append([''.join(title.split()),k["bvid"],video_path])
        Download_Video.start(video_list)
        print(video_list)
        page += 1


#用户个人主页信息
def main(mid):
    wts = int(time.time())
    w_rid = execjs.compile(open('./e.js','r',encoding='utf-8').read()).call('md5',wts)
    headers = {
        'mid': mid,
        'token': '',
        'platform': 'web',
        'w_rid': w_rid,
        'wts': str(wts),
        'origin': 'https://space.bilibili.com',
        'referer': f'https://space.bilibili.com/{mid}',
        'user-agent': UserAgent().random
    }
    information = {}
    #用户主页
    url = f'https://api.bilibili.com/x/space/wbi/acc/info?mid={mid}&token=&platform=web&w_rid={w_rid}&wts={wts}'
    resp = requests.get(url=url,headers=headers).json()
    information["姓名"] = resp["data"]["name"]
    information["id"] = resp["data"]["mid"]
    information["生日"] = resp["data"]["birthday"]
    information["性别"] = resp["data"]["sex"]
    information["简介"] = resp["data"]["sign"]
    information["等级"] = resp["data"]["level"]
    information["个人标签"] = resp["data"]["tags"]
    try:
        information["分区"] = resp["data"]["official"]["title"]
    except:
        pass
    information["会员"] = resp["data"]["vip"]["label"]["text"]
    #获取关注数量和粉丝数量
    url = f'https://api.bilibili.com/x/relation/stat?vmid={mid}&jsonp=jsonp'
    resp = requests.get(url=url,headers=headers).json()
    information["关注"] = resp["data"]["following"]
    information["粉丝数量"] = resp["data"]["follower"]
    url = f'https://api.bilibili.com/x/space/notice?mid={mid}&jsonp=jsonp'
    resp = requests.get(url=url,headers=headers).json()
    information["公告"] = resp["data"]
    try:
        os.mkdir('./'+information["姓名"])
    except:
        pass
    path = os.getcwd() + '/'
    with open(path+information["姓名"]+'/信息.json','w',encoding='utf-8') as f:
        f.write(json.dumps(information,ensure_ascii=False))
    return path+information["姓名"]+'/'

#uid的唯一性
def ID():
    mid = input("请输入要查询用户的ID:")
    video_path = main(mid)
    video(mid,video_path,page=1)

#返回用户名的查询结果
def name_id(keyword,page):
    wts = int(time.time())
    w_rid = execjs.compile(open('./e.js','r',encoding='utf-8').read()).call('md5',wts)
    headers = {
            'w_rid': w_rid,
            'wts': str(wts),
            'user-agent': UserAgent().random
        }
    url = f'https://api.bilibili.com/x/web-interface/wbi/search/type?__refresh__=true&_extra=&context=&page={page}&page_size=36&order=&duration=&from_source=&from_spmid=333.337&platform=pc&highlight=1&single_column=0&keyword={keyword}&ad_resource=&source_tag=3&category_id=&search_type=bili_user&order_sort=0&user_type=0&dynamic_offset=0&w_rid={w_rid}&wts={wts}'
    return requests.get(url=url,headers=headers).json()

if __name__ == "__main__":
    print('用户名输入 name, UID号码请输入 id')
    name_uid = input('选者输入用户名还是UID号码:')
    if name_uid == 'name':
        keyword = input('请输入查询用户名:')
        page = 1
        resp = name_id(keyword,page)
        for k in resp["data"]["result"]:
            print(k["uname"]+':'+str(k["mid"]))
        while 1:
            print()
            print('请输入确认用户名对应的数字号码:')
            print('若没有,请输入 next')
            print('要退出,请输入 c ')
            print()
            n = input('请输入:')
            if n == 'next':
                page += 1
                resp = name_id(keyword,page)
                for k in resp["data"]["result"]:
                    print(k["uname"]+':'+str(k["mid"]))
            elif n == 'c':
                break
            else:
                mid = n
                video_path = main(mid)
                video(mid,video_path,page=1)
                break
    elif name_uid == 'id':
        ID()
    else:
        print('输入错误')
        




