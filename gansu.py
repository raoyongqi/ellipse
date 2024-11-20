import arcpy
from arcpy.sa import *
import os

# 设置环境
# arcpy.env.overwriteOutput = True  # 允许覆盖输出文件
# arcpy.CheckOutExtension("Spatial")  # 检查和启用 Spatial Analyst 扩展

# 输入栅格数据路径
input_raster = r"C:\Users\r\Desktop\cal\gansu\gansu\gansu_Ci_2001.tif"  # 栅格文件路径
output_raster = r"C:\Users\r\Desktop\cal\gansu\extract\gansu_Ci_2001_output.tif"  # 输出栅格文件路径

# 检查输出文件夹是否存在，不存在则创建
output_raster_folder = os.path.dirname(output_raster)  # 获取输出文件夹路径
if not os.path.exists(output_raster_folder):
    os.makedirs(output_raster_folder)

# 创建栅格对象
raster = arcpy.Raster(input_raster)

# 使用 Con 函数进行条件转换：将值为 -1 的像元替换为 NoData，其他值保持原样
# 这里我们使用 SetNull 函数将 -1 替换为 NoData
output = Con(raster == -1, SetNull(raster == -1, raster), raster)

# 保存输出栅格
output.save(output_raster)
