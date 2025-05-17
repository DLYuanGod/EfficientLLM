import openpyxl
import json

# 读取Excel文件
wb = openpyxl.load_workbook('forms/工作簿1.xlsx')
ws = wb.active

# 获取数据
data = []
for row in ws.iter_rows(min_row=1, values_only=True):
    # 不跳过空行，保持原始数据
    row_data = []
    for cell in row:
        # 直接添加原始值，不做处理
        row_data.append(cell)
    data.append(row_data)

# 将数据转换为JSON并打印
print(json.dumps(data, default=lambda x: str(x) if x is not None else None, ensure_ascii=False)) 