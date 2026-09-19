import pandas as pd
import matplotlib.pyplot as plt

# 读取已经爬好的数据
df = pd.read_excel("douban_top250.xlsx")

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

# ===== 分析：哪个年代的电影平均评分最高 =====
df["年份"] = pd.to_numeric(df["年份"], errors="coerce")
df_year = df.dropna(subset=["年份"]).copy()

def get_decade(year):
    return f"{int(year // 10 * 10)}年代"

df_year["年代"] = df_year["年份"].apply(get_decade)
decade_avg = df_year.groupby("年代")["评分"].mean().sort_index()

print("各年代平均评分：")
print(decade_avg)

plt.figure(figsize=(10, 6))
plt.bar(decade_avg.index, decade_avg.values, color="steelblue")
plt.xlabel("年代")
plt.ylabel("平均评分")
plt.title("豆瓣Top250中各年代电影平均评分")
plt.ylim(8.5, 9.8)
plt.tight_layout()
plt.show()