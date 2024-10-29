import json

# todo 定义读取和写入文件的路径
input_file = 'Devign_func.json'  # 输入文件路径
output_file = input_file  # 输出文件路径

# 读取 JSON 文件
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 过滤掉没有 "slice" 键或 "slice" 中 "result" 为空列表的样本
filtered_data = [
    item for item in data 
    if "slice" in item and "result" in item["slice"] and item["slice"]["result"]
]

# 将过滤后的数据写入新的 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(filtered_data, f, ensure_ascii=False, indent=4)

print(f"过滤完成，保留了 {len(filtered_data)} 个含有 'slice' 键且 'result' 不为空的样本。")