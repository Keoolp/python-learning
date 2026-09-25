import pandas as pd
import jieba
import re
import matplotlib.pyplot as plt
from collections import Counter

# 添加自定义词典，让jieba认识这些专有名词
#要在第一次运行测试之后看看什么常用专有名词被jieba割掉了
jieba.add_word("沃雅妮莎")
jieba.add_word("真珠")
jieba.add_word("星穹铁道")
jieba.add_word("崩坏星穹铁道")
jieba.add_word("粤韵风华")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 读取数据
df = pd.read_csv("bili_hot.csv", encoding="utf-8-sig")

# 2. 分组
game = ["手机游戏", "单机游戏", "网络游戏", "电子竞技"]
life = ["日常", "搞笑", "出行"]

df_game = df[df["分区"].isin(game)]
df_life = df[df["分区"].isin(life)]

print(f"游戏类：{len(df_game)} 条")
print(f"生活类：{len(df_life)} 条")

# ===== 图1：平均播放量对比 =====
avg_game = df_game["播放量"].mean()
avg_life = df_life["播放量"].mean()

plt.figure(figsize=(8, 6))
plt.bar(["游戏类", "生活类"], [avg_game, avg_life], color=["steelblue", "coral"])
plt.ylabel("平均播放量")
plt.title("游戏类 vs 生活类：平均播放量对比", fontsize=16, fontweight='bold')
for i, v in enumerate([avg_game, avg_life]):
    plt.text(i, v + 10000, f"{v/10000:.1f}万", ha='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("对比_平均播放量.png", dpi=150, bbox_inches="tight")

# ===== 图2：标题平均长度对比 =====
len_game = df_game["标题"].str.len().mean()
len_life = df_life["标题"].str.len().mean()

plt.figure(figsize=(8, 6))
plt.bar(["游戏类", "生活类"], [len_game, len_life], color=["steelblue", "coral"])
plt.ylabel("平均标题长度（字数）")
plt.title("游戏类 vs 生活类：标题平均长度对比", fontsize=16, fontweight='bold')
for i, v in enumerate([len_game, len_life]):
    plt.text(i, v + 0.3, f"{v:.1f}字", ha='center', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("对比_标题长度.png", dpi=150, bbox_inches="tight")

# ===== 图3：高频词对比 =====
def get_top_words(titles, n=10):
    words = []
    for t in titles:
        words.extend(jieba.lcut(t))
    words = [w for w in words if re.match(r'^[\u4e00-\u9fa5a-zA-Z0-9]+$', w) and len(w) > 1]
    stop_words = ["的", "了", "是", "在", "我", "你", "他", "这", "那", "有", "和", "就", "都",
                  "一个", "到底", "什么", "竟然", "我们", "还有", "系列", "居然", "如何", "怎么",
                  "为什么", "可以", "不是", "没有", "这个", "那个", "自己", "已经", "因为",
                  "所以", "但是", "如果", "视频", "一次", "一直", "真的", "感觉", "知道"]
    words = [w for w in words if w not in stop_words]
    return Counter(words).most_common(n)

top_game = get_top_words(df_game["标题"].tolist())
top_life = get_top_words(df_life["标题"].tolist())

print("\n游戏类高频词：")
for w, c in top_game:
    print(f"  {w}: {c}")

print("\n生活类高频词：")
for w, c in top_life:
    print(f"  {w}: {c}")

# 对比柱状图
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

words_g = [w[0] for w in top_game][::-1]
counts_g = [w[1] for w in top_game][::-1]
axes[0].barh(words_g, counts_g, color="steelblue")
axes[0].set_title("游戏类高频词TOP10", fontsize=14, fontweight='bold')
axes[0].set_xlabel("出现次数")

words_l = [w[0] for w in top_life][::-1]
counts_l = [w[1] for w in top_life][::-1]
axes[1].barh(words_l, counts_l, color="coral")
axes[1].set_title("生活类高频词TOP10", fontsize=14, fontweight='bold')
axes[1].set_xlabel("出现次数")

plt.tight_layout()
plt.savefig("对比_高频词.png", dpi=150, bbox_inches="tight")

plt.show()