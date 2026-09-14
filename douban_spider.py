import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

url = "https://movie.douban.com/top250"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

response = requests.get(url, headers=headers)
print(f"状态码: {response.status_code}")

if response.status_code == 200:
    print("抓取成功！正在解析网页...")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # 找到所有电影条目
    items = soup.find_all("div", class_="item")
    
    movie_list = []
    for item in items:
        # 提取中文片名
        title_tag = item.find("span", class_="title")
        if title_tag:
            title = title_tag.text.strip()
        else:
            continue
        
        # 提取评分
        rating_tag = item.find("span", class_="rating_num")
        rating = rating_tag.text.strip() if rating_tag else "暂无"
        
        # 提取评价人数（在 <span> 标签中，位于 rating_num 之后）
        # 直接在当前电影条目里找所有的 <span>，然后筛选
        all_spans = item.find_all("span")
        people = "暂无"
        for span in all_spans:
            text = span.text.strip()
            if "人评价" in text:
                people = text[:-3]  # 去掉 "人评价" 三个字
                break
        
        # 提取导演和年份
        bd = item.find("div", class_="bd")
        info_tag = bd.find("p") if bd else None
        
        director = "暂无"
        year = "暂无"
        
        if info_tag:
            info = info_tag.text.strip()
            # 用 "/" 分割信息，获取导演和年份
            parts = info.split("/")  # 定义 parts 变量！
            
            # 方法：找“导演”和“主演”之间的内容
            if "导演" in info:
                # 取“导演”之后的内容
                start = info.find("导演")
                # 如果“主演”存在，就取到“主演”之前；否则取到字符串末尾
                if "主演" in info:
                    end = info.find("主演")
                    director = info[start:end].strip()
                else:
                    director = info[start:].strip()
            
            # 年份通常在 parts 的最后，但可能会包含国家信息，我们提取纯数字年份
            for part in parts:
                # 如果这一部分包含4位数字，就认为是年份
                year_match = re.search(r'\d{4}', part)
                if year_match:
                    year = year_match.group()
                    break
        
        movie_list.append({
            "片名": title,
            "评分": rating,
            "评价人数": people,
            "导演": director,
            "年份": year
        })
    
    # 保存到 Excel
    df = pd.DataFrame(movie_list)
    df.to_excel("douban_top250.xlsx", index=False)
    df["评分"] = pd.to_numeric(df["评分"], errors="coerce")
    print(f"成功保存 {len(movie_list)} 部电影到 douban_top250.xlsx")
    # ===== 新增：生成图表 =====
    # 评分最高的10部电影
    # ===== 生成图表 =====
    import matplotlib.pyplot as plt

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
    plt.rcParams['axes.unicode_minus'] = False

    # 使用更现代的样式
    top10 = df.nlargest(10, "评分")

    fig, ax = plt.subplots(figsize=(12, 7))

    # 绘制条形图，用渐变色
    bars = ax.barh(top10["片名"], top10["评分"], color=plt.cm.Blues([0.4 + 0.05*i for i in range(10)]))

    # 在条形上显示评分
    for bar, rating in zip(bars, top10["评分"]):
        ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2, 
                f'{rating:.1f}', ha='left', va='center', fontsize=11, fontweight='bold')

    ax.set_xlabel('评分', fontsize=12)
    ax.set_title('豆瓣Top250中评分最高的10部电影', fontsize=16, fontweight='bold')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    # 反转 y 轴，让最高的在上面
    ax.invert_yaxis()
    plt.tight_layout()
    plt.show()
else:
    print("抓取失败，状态码：", response.status_code)

