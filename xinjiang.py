import arcpy
from arcpy.sa import *
import os

# 设置环境
arcpy.env.overwriteOutput = True  # 允许覆盖输出文件
arcpy.CheckOutExtension("Spatial")  # 检查并启用 Spatial Analyst 扩展

# 输入文件夹路径（存放所有输入的 tiff 文件）
input_folder = r"C:\Users\r\Desktop\cal\xinjiang\xinjiang_Ci"  # 输入文件夹路径
output_folder = r"C:\Users\r\Desktop\cal\xinjiang\extract"  # 输出文件夹路径

# 获取输入文件夹中的所有 .tif 文件
tif_files = [f for f in os.listdir(input_folder) if f.endswith(".tif")]

# 检查输出文件夹是否存在，不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历每个 tif 文件进行处理
for tif_file in tif_files:
    # 构造输入栅格文件和输出栅格文件的完整路径
    input_raster = os.path.join(input_folder, tif_file)
    output_raster = os.path.join(output_folder, f"{os.path.splitext(tif_file)[0]}_output.tif")
    
    print(f"正在处理文件: {tif_file}")
    
    # 创建栅格对象
    raster = arcpy.Raster(input_raster)
    
    # 使用 Con 函数进行条件转换：将值为 -1 的像元替换为 NoData，其他值保持原样
    # 这里我们使用 SetNull 函数将 -1 替换为 NoData
    output = Con(raster == -1, SetNull(raster == -1, raster), raster)
    
    # 保存输出栅格
    output.save(output_raster)
    
    print(f"输出栅格已保存: {output_raster}")

print("批量处理完成！")
