#b站某个分区的排行榜第一页

import requests
import pandas as pd
import time

url = "https://api.bilibili.com/x/web-interface/ranking/v2"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com/"
}
#去b站排行榜界面知识分区找到rid
rid = 1010
params = {
    "rid": rid,  
    "type": "all"
}

response = requests.get(url, headers=headers, params=params, timeout=10)
data = response.json()

if data["code"] == 0:
    videos = data["data"]["list"]
    all_videos = []
    for v in videos:
        all_videos.append({
            "标题": v["title"],
            "播放量": v["stat"]["view"],
            "UP主": v["owner"]["name"],
            "分区": v["tname"],
            "链接": f"https://www.bilibili.com/video/{v['bvid']}"
        })
    df = pd.DataFrame(all_videos)
    #保存csv文件为“bili_ranking_ridXX.csv”
    df.to_csv(f"bili_ranking_rid{rid}.csv", index=False, encoding="utf-8-sig")
    print(f"共保存 {len(all_videos)} 条排行榜数据到 bili_ranking.csv")
else:
    print(f"请求失败：{data['message']}")