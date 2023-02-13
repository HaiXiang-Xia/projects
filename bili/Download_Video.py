import requests
import os
import json
import re
from fake_useragent import UserAgent
from concurrent.futures import ProcessPoolExecutor


headers = {
    'referer': 'https://www.bilibili.com/',
    'user-agent': UserAgent().random,
}

#成功爬取的视频名称
set_1 = {}


#视频，音频 合并
def video_audio(video,audio,name):
    print(name.split('/')[-1]+'下载完毕，音视频合成中')
    os.system('ffmpeg -i ' + video + ' -i ' + audio + ' -acodec copy -vcodec copy ' + name +'.mp4 -loglevel quiet')
    true = True
    if true:
        try:
            os.remove(video)
            os.remove(audio)
            print('删除源文件')
        except:
            print('删除源文件失败')
    return name.split('/')[-1]+'视频合成结束'

#下载
def download(videourl,audiourl,name,Bv,path_Bv):
    print('视频下载中...')
    path = path_Bv+'video/'
    video = path+name+Bv+'.mp4'
    audio = path+name+Bv+'.mp3'
    try:
        os.mkdir(path)
    except:
        pass
    date_mp4 = requests.get(url=videourl,headers=headers).content
    with open(video,'wb') as f:
        f.write(date_mp4)
    date_mp3 = requests.get(url=audiourl,headers=headers).content
    with open(audio,'wb') as f:
        f.write(date_mp3)
    return video_audio(video,audio,path+name)

#传入视频网址    
def main(url,name,path_BV):
    date = requests.get(url=url,headers=headers).text
    str_date = re.findall('window.__playinfo__=(.*?)</script>',date)[0]
    content = json.loads(str_date)
    videourl = content['data']['dash']['video'][0]['baseUrl']
    audiourl = content['data']['dash']['audio'][0]['baseUrl']
    Bv = url.split('/')[4]
    return download(videourl,audiourl,name,Bv,path_BV)

#视频信息列表
def start(name_url):
    s = open(name_url[0][2]+'config.json','a',encoding='utf-8')
    s.close()
    try:
        #打开已下载视频的 字符串
        with open(name_url[0][2]+'config.json','r',encoding='utf-8') as f:
            set_Bv = json.loads(f.read())
    except:
        set_Bv = {}
    number = os.cpu_count()
    p = ProcessPoolExecutor(number)
    res = []
    for i in name_url:
        if i[1] not in set_Bv.values():
            set_1[i[0]] = i[1]
            url = 'https://www.bilibili.com/video/'+i[1]+'/'
            future = p.submit(main,url,i[0],i[2])
            res.append(future)
    p.shutdown()
    with open(name_url[0][2]+'config.json','w',encoding='utf-8') as f:
        f.write(json.dumps(set_1,ensure_ascii=False))

    for r in res:
        print(r.result())