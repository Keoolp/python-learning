import pandas as pd
import jieba
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取爬好的CSV（爆款标题）
df = pd.read_csv("bili_hot.csv", encoding="utf-8-sig")
titles = df["标题"].dropna().tolist()

# 2. 用jieba分词：把每个标题拆成一个个词
words = []
for title in titles:
    words.extend(jieba.lcut(title))
# 循环结束后统一过滤,只保留中文、英文、数字的词，且长度>1
words = [w for w in words if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]+$', w) and len(w) > 1]

# 3. 去掉单字、空格、无意义的口语化的填充词
stop_words = [
    "的", "了", "是", "在", "我", "你", "他", "这", "那", "有", "和", "就", "都",
    "一个", "到底", "什么", "竟然", "我们", "还有", "系列", "居然", "如何", "怎么",
    "为什么", "可以", "不是", "没有", "这个", "那个", "自己", "已经", "因为",
    "所以", "但是", "如果", "视频", "一次", "一直", "真的", "感觉", "知道", "这么","bilibili","就是"
]
# 过滤掉上面的那些stop_words
words = [w for w in words if w not in stop_words]
# 4. 统计每个词出现了多少次
word_counts = Counter(words)
top_words = word_counts.most_common(20) #most_common(20) ：把词频最高的前20个词从高到低排好，返回一个列表

print("高频词TOP20：")
for word, count in top_words:
    print(f"{word}: {count}")

# 5. 生成词云图，词越大出现越多
wc = WordCloud(
    font_path="C:/Windows/Fonts/msyh.ttc",   # 微软雅黑
    width=1000,
    height=700,
    background_color="#f5f5f5",
    max_words=80,
    colormap="viridis", 
    random_state=42
)
wc.generate_from_frequencies(word_counts)

plt.figure(figsize=(10, 8))  #创建一个画布，宽10英寸、高8英寸
plt.imshow(wc, interpolation="bilinear")  #把生成的词云wc画到画布上。interpolation="bilinear" 是让图片显示更平滑、不锯齿
plt.axis("off")  #关掉坐标轴（词云图不需要x轴、y轴）
plt.title("B站热门视频标题词云", fontsize=16, fontweight='bold')  #设置标题，字号16，加粗
plt.savefig("标题词云图.png", dpi=150, bbox_inches="tight")  #把画布存为图片，dpi=150让图片更清晰，bbox_inches="tight" 去白边
plt.show()  #显示这张图

# 6. 生成高频词柱状图
words_top = [w[0] for w in top_words]  #遍历 top_words 里的每一个元组 w，把 w[0]（也就是词）拿出来，组成一个新列表
counts_top = [w[1] for w in top_words]  #遍历 top_words 里的每一个元组 w，把 w[1]（也就是次数）拿出来，组成一个新列表

plt.figure(figsize=(10, 6))
#画横向柱状图。[::-1] 是把列表倒过来，这样出现次数最多的词会显示在最上面。颜色用钢蓝色
plt.barh(words_top[::-1], counts_top[::-1], color="steelblue")   #第一个参数：y轴上的标签（词）,第二个参数：x轴上的长度（次数）
plt.xlabel("出现次数") #设置x轴标签为“出现次数”
plt.title("B站热门视频标题高频词TOP20", fontsize=16, fontweight='bold')
plt.tight_layout()  #自动调整布局，防止文字被裁掉
plt.savefig("标题高频词柱状图.png", dpi=150, bbox_inches="tight")
plt.show()