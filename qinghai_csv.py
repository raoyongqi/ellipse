import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体，防止出现乱码
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体字体
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

# 读取CSV文件
csv_file = r'C:\Users\r\Desktop\cal\qinghai\qinghai_centers.csv'  # 替换为你的CSV文件路径
data = pd.read_csv(csv_file)

# 提取年份、经度和纬度
years = data['year']
center_x = data['Center X']
center_y = data['Center Y']

# 创建一个图形
plt.figure(figsize=(10, 6))

# 绘制经纬度变化（经度作为x，纬度作为y）
plt.plot(center_x, center_y, label='中心坐标', marker='o', color='b')

# 为每个数据点添加年份标签
for i in range(len(years)):
    plt.text(center_x[i], center_y[i], str(years[i]), color='black', fontsize=18, ha='right', va='bottom')

# 添加标题和标签
plt.title('青海省植被覆盖度重心的空间迁移特征（2001-2020年）')
plt.xlabel('经度（Center X）', fontsize=16)  # X轴标签字体大小
plt.ylabel('纬度（Center Y）', fontsize=16)  # Y轴标签字体大小

# 调整刻度标签的字体大小
plt.tick_params(axis='both', labelsize=16, width=2)  # 设置x轴和y轴刻度标签字体大小和刻度线宽度


# 显示网格
plt.grid(True)

# 添加图例
plt.legend()
plt.savefig('qinghai_move.png')  # 保存图表

# 显示图形
plt.show()
