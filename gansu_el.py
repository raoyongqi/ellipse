import arcpy
import numpy as np
import math
import os

# 设置环境
arcpy.env.overwriteOutput = True

# 输入栅格数据路径
input_raster = r"C:\Users\r\Desktop\cal\gansu\extract\gansu_Ci_2001_output.tif"  # 输出栅格文件路径
output_point = r"C:\Users\r\Desktop\cal\gansu\dot\gansu_Ci_2001_output.shp"  # 输出点数据路径
output_fc = r"C:\Users\r\Desktop\cal\gansu\el\gansu_Ci_2001_output.shp"# 输出椭圆 Shapefile 路径
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

# 获取点数据的坐标
points = []
fields = ['SHAPE@X', 'SHAPE@Y']  # 获取点的 X 和 Y 坐标

with arcpy.da.SearchCursor(output_point, fields) as cursor:
    for row in cursor:
        points.append((row[0], row[1]))

# 将点数据转换为 Numpy 数组
points = np.array(points)

# 计算点数据的均值（即中心点坐标）
mean_x = np.mean(points[:, 0])
mean_y = np.mean(points[:, 1])

# 计算点数据的协方差矩阵
cov_matrix = np.cov(points[:, 0], points[:, 1])

# 计算协方差矩阵的特征值和特征向量
eigvals, eigvecs = np.linalg.eig(cov_matrix)

# 使用最大的特征值来决定椭圆的长轴，次特征值决定短轴
axis_length_major = 2 * math.sqrt(eigvals[0])  # 主轴长度
axis_length_minor = 2 * math.sqrt(eigvals[1])  # 次轴长度

# 计算旋转角度（椭圆的方向）
angle = math.atan2(eigvecs[1, 0], eigvecs[0, 0])  # 旋转角度（弧度）

# 输出标准差椭圆的参数
print(f"椭圆主轴长度：{axis_length_major}")
print(f"椭圆次轴长度：{axis_length_minor}")
print(f"椭圆方向角度：{math.degrees(angle)}°")

# 步骤 3: 生成标准差椭圆并保存为 Shapefile
print("生成标准差椭圆并保存为 Shapefile...")

# 创建一个新的 Feature Class 来保存椭圆
arcpy.management.CreateFeatureclass(os.path.dirname(output_fc), os.path.basename(output_fc), "POLYGON")

# 创建椭圆的角度转换为度
angle_deg = math.degrees(angle)

# 使用 ArcPy 创建椭圆的几何坐标
# 椭圆的中心坐标为 mean_x, mean_y，主轴、次轴和旋转角度已经计算
ellipse_points = []
num_points = 100  # 用于构造椭圆的点数，更多的点会让椭圆更平滑

# 计算椭圆的角度范围，生成椭圆坐标
for i in range(num_points):
    theta = 2 * math.pi * i / num_points
    x = mean_x + axis_length_major * math.cos(theta) * math.cos(angle_deg) - axis_length_minor * math.sin(theta) * math.sin(angle_deg)
    y = mean_y + axis_length_major * math.cos(theta) * math.sin(angle_deg) + axis_length_minor * math.sin(theta) * math.cos(angle_deg)
    ellipse_points.append(arcpy.Point(x, y))

# 创建椭圆的 Polygon 对象
ellipse_array = arcpy.Array(ellipse_points)
ellipse_polygon = arcpy.Polygon(ellipse_array)

# 将椭圆插入到 Feature Class 中
with arcpy.da.InsertCursor(output_fc, ["SHAPE@"]) as cursor:
    cursor.insertRow([ellipse_polygon])

print(f"标准差椭圆已保存为 Shapefile: {output_fc}")
