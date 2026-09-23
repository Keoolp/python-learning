import requests
import pandas as pd
import time

# B站热门视频接口地址 （url = "..."	告诉程序要去哪个接口拿数据）
url = "https://api.bilibili.com/x/web-interface/popular"

# 伪装成浏览器，防止被B站拦截
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}

# 用来存所有视频数据
all_videos = []

# 爬取前50页，每页20条
for pn in range(1, 51):
    params = {
        "ps": 20,   # 每页20条
        "pn": pn    # 第几页
    }
    
    # 发送请求，拿回JSON数据
    response = requests.get(url, headers=headers, params=params, timeout=10)
    data = response.json()
    
    # code == 0 表示请求成功
    if data["code"] == 0:
        videos = data["data"]["list"]  #从JSON里取出视频列表
        for v in videos:
            #all_videos.append({...}) 把提取的数据存进总列表
            all_videos.append({
                "标题": v["title"],
                "播放量": v["stat"]["view"],
                "UP主": v["owner"]["name"],
                "分区": v["tname"],
                "链接": f"https://www.bilibili.com/video/{v['bvid']}"
            })
        print(f"第 {pn} 页爬取成功，共 {len(videos)} 条")
    else:
        print(f"第 {pn} 页爬取失败：{data['message']}")
    
    time.sleep(2)   # 每页间隔2秒，避免请求太快被B站限制

# 保存到 CSV 文件
df = pd.DataFrame(all_videos)
df.to_csv("bili_hot.csv", index=False, encoding="utf-8-sig")
print(f"共保存 {len(all_videos)} 条视频数据到 bili_hot.csv")