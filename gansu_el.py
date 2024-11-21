import arcpy
import numpy as np
import math
import os

# 设置环境
# 输入栅格数据路径
input_raster = r"C:\Users\r\Desktop\cal\gansu\extract\gansu_Ci_2001_output.tif"  # 输入栅格文件路径
output_point = r"C:\Users\r\Desktop\cal\gansu\dot\gansu_Ci_2001_output.shp"  # 输出点数据路径
output_fc = r"C:\Users\r\Desktop\cal\gansu\el\gansu_Ci_2001_output.shp"  # 输出椭圆 Shapefile 路径

# 检查输出文件夹是否存在，不存在则创建
output_point_folder = os.path.dirname(output_point)  # 获取输出文件夹路径
if not os.path.exists(output_point_folder):
    os.makedirs(output_point_folder)

output_fc_folder = os.path.dirname(output_fc)  # 获取输出文件夹路径
if not os.path.exists(output_fc_folder):
    os.makedirs(output_fc_folder)

# 步骤 1: 将栅格数据转换为点数据
print("转换栅格数据为点数据...")
arcpy.RasterToPoint_conversion(input_raster, output_point, "VALUE")
print("栅格数据已转换为点数据。")

# 步骤 2: 计算点数据的协方差矩阵，并提取标准差椭圆的长短轴和旋转角度
print("计算点数据的协方差矩阵...")

# 获取点数据的坐标和权重（VALUE 字段作为权重）
points = []
weights = []  # 用于存储权重

fields = ['SHAPE@X', 'SHAPE@Y', 'grid_code']  # 获取点的 X、Y 坐标和 VALUE 字段

with arcpy.da.SearchCursor(output_point, fields) as cursor:
    for row in cursor:
        points.append([row[0], row[1]])  # 提取坐标
        weights.append(row[2])  # 提取 VALUE 字段作为权重

# 转换为 NumPy 数组
points = np.array(points)
weights = np.array(weights)

# 计算加权均值（考虑权重）
mean_x = np.average(points[:, 0], weights=weights)
mean_y = np.average(points[:, 1], weights=weights)
# 打印椭圆的中心坐标
print(f"椭圆的中心坐标: ({mean_x}, {mean_y})")

# 将点坐标居中
centered_points = points - np.array([mean_x, mean_y])

# 计算加权协方差矩阵
cov_matrix = np.cov(centered_points.T, aweights=weights)

# 计算协方差矩阵的特征值和特征向量
eigenvalues, eigenvectors = np.linalg.eig(cov_matrix)

# 计算半长轴和半短轴
semi_major = np.sqrt(np.max(eigenvalues))
semi_minor = np.sqrt(np.min(eigenvalues))

# 计算椭圆的旋转角度（主轴的角度）
theta = np.arctan2(eigenvectors[1, np.argmax(eigenvalues)], eigenvectors[0, np.argmax(eigenvalues)])

# 打印结果
print(f"Semi-major axis: {semi_major}")
print(f"Semi-minor axis: {semi_minor}")
print(f"Rotation angle (radians): {theta}")
print(f"Rotation angle (degrees): {np.degrees(theta)}")

# 创建一个新的 Feature Class 来保存椭圆
arcpy.management.CreateFeatureclass(os.path.dirname(output_fc), os.path.basename(output_fc), "POLYGON")

# 将角度转换为度
angle_deg = np.degrees(theta)

# 使用 ArcPy 创建椭圆的几何坐标
ellipse_points = []
num_points = 100  # 用于构造椭圆的点数，更多的点会让椭圆更平滑

# 计算椭圆的角度范围，生成椭圆坐标
for i in range(num_points):
    angle = 2 * math.pi * i / num_points
    x = mean_x + semi_major * math.cos(angle) * math.cos(theta) - semi_minor * math.sin(angle) * math.sin(theta)
    y = mean_y + semi_major * math.cos(angle) * math.sin(theta) + semi_minor * math.sin(angle) * math.cos(theta)
    ellipse_points.append(arcpy.Point(x, y))

# 创建椭圆的 Polygon 对象
ellipse_array = arcpy.Array(ellipse_points)
ellipse_polygon = arcpy.Polygon(ellipse_array)

# 将椭圆插入到 Feature Class 中
with arcpy.da.InsertCursor(output_fc, ["SHAPE@"]) as cursor:
    cursor.insertRow([ellipse_polygon])

print(f"标准差椭圆已保存为 Shapefile: {output_fc}")
