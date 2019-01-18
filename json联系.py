import requests
import json
import psycopg2
import math
import os
import http.cookiejar


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
}
#获取专辑信息
def get_trackId(albumId,pageNum):
    url = 'https://www.ximalaya.com/revision/album/getTracksList?albumId=' + str(albumId) + '&pageNum=' + str(pageNum)
    requeste = requests.get(url,headers=headers)
    json_dict = requeste.json()
    track = json_dict['data']['tracks']
    global trackTotalCount
    trackTotalCount = json_dict['data']['trackTotalCount']
    global pageNumCount
    pageNumCount = json_dict['data']['pageNum']
    global page
    page = math.ceil(trackTotalCount / 30)
    list = []
    for ts in track:
        list.append({'trackId':ts['trackId'],'title':ts['title']})
    return list

#获取专辑名称
def get_Title(albumid):
    url = 'https://www.ximalaya.com/revision/album?albumId=' + str(albumid)
    requeste = requests.get(url,headers=headers)
    json_dict = requeste.json()
    albumtitle = json_dict['data']['mainInfo']['albumTitle']
    return albumtitle



#获取下载链接
def get_track_url(trackId):
    url = 'https://www.ximalaya.com/revision/play/tracks?trackIds=' + str(trackId)
    resp = requests.get(url,headers=headers)
    result = resp.json()
    tracksForAudioPlay = result['data']['tracksForAudioPlay']
    if len(tracksForAudioPlay) > 0:
        return tracksForAudioPlay[0]['src']

#下载链接
def download_track(url,file):
    resp = requests.get(url,headers=headers,stream=True)
    with open(file,'wb') as f:
        for data in resp.iter_content(chunk_size=1024):
            if data: f.write(data)




# 输入声音编码        
albumId = input('声音编号：')
# 初始化第一位页面
pageNum = 1
tracks = get_trackId(albumId,pageNum)
title = get_Title(albumId)
print(title)
print("总集数：" + str(trackTotalCount) )
print("总页数：" + str(page))
print("当前页面" + str(pageNumCount))
#创建标题文件夹无就创建
if not os.path.exists(title):
    os.mkdir(title)
#下载目录选择标题文件夹
dir = title
#开始第一个页面的下载
for track in tracks:
    trackUrl = get_track_url(track['trackId'])
    if trackUrl:
        ext = trackUrl[trackUrl.rindex('.'):]
        file_path = dir + "/" + track['title'] + ext
        print('正在下载：' + trackUrl)
        download_track(trackUrl,file_path)
#开始所有页面的循环下载
while pageNumCount != page:
    pageNum = pageNum+1
    tracks = get_trackId(albumId,pageNum)
    print("总集数：" + str(trackTotalCount) )
    print("总页数：" + str(page))
    print("当前页面" + str(pageNumCount))
    for track in tracks:
        trackUrl = get_track_url(track['trackId'])
        if trackUrl:
            ext = trackUrl[trackUrl.rindex('.'):]
            file_path = dir +"/"+ track['title'] + ext
            print('正在下载：' + trackUrl)
            download_track(trackUrl,file_path)
            if pageNum == page:
                print("下载完成")