import pandas as pd
import matplotlib.pyplot as plt

# 读取已经爬好的数据
df = pd.read_excel("douban_top250.xlsx")


# ====生成图表:评分最高的10部电影======
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

#从 df 这个表格里，按“评分”列降序取出前 10 行，存到 top10 这个新变量里
top10 = df.nlargest(10, "评分")
#创建一个“画布”和“坐标系”，设置画布大小为 12 英寸宽、7 英寸高
fig, ax = plt.subplots(figsize=(12, 7))

# 绘制条形图，颜色深浅随排名变化
bars = ax.barh(top10["片名"], top10["评分"], color=plt.cm.Blues([0.4 + 0.05*i for i in range(10)]))

# 用ax.text(...) 在每个条形右侧显示评分
for bar, rating in zip(bars, top10["评分"]):
    ax.text(bar.get_width() + 0.03, bar.get_y() + bar.get_height()/2, 
            f'{rating:.1f}', ha='left', va='center', fontsize=11, fontweight='bold')

#设置字体大小(fontsize)、字体加粗(fontweight='bold')
ax.set_xlabel('评分', fontsize=12)
ax.set_title('豆瓣Top250中评分最高的10部电影', fontsize=16, fontweight='bold')
#增加网格线
ax.grid(axis='x', linestyle='--', alpha=0.6)

# 反转 y 轴，让最高的在上面
ax.invert_yaxis()
#去掉多余的白边
plt.tight_layout()
#dpi=150让图片更清晰
fig.savefig("analyze2(top10_movies).png", dpi=150, bbox_inches="tight")   # ← 用 fig 保存
#先保存再显示
plt.show()

