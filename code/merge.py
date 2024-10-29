import json

# 定义文件路径
devign_file = 'Devign_func.json'
reveal_non_vul_file = 'Reveal_non_vul_func.json'
reveal_vul_file = 'Reveal_vul_func.json'

# 定义一个函数来读取 JSON 文件
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# 读取 JSON 文件
devign_data = load_json(devign_file)
reveal_non_vul_data = load_json(reveal_non_vul_file)
reveal_vul_data = load_json(reveal_vul_file)

# 存储最终合并的数据
merged_data = []

# 处理 Devign_func.json 数据
for item in devign_data:
    merged_item = {
        'code': item['func'],
        'slice': item['slice'],
        'label': 0 if item['target'] == 1 else 1
    }
    merged_data.append(merged_item)

# 处理 Reveal_non_vul_func.json 数据
for item in reveal_non_vul_data:
    merged_item = {
        'code': item['code'],
        'slice': item['slice'],
        'label': 0
    }
    merged_data.append(merged_item)

# 处理 Reveal_vul_func.json 数据
for item in reveal_vul_data:
    merged_item = {
        'code': item['code'],
        'slice': item['slice'],
        'label': 1
    }
    merged_data.append(merged_item)

# 输出到新的 JSON 文件
output_file = 'cotvd.json'
with open(output_file, 'w') as f:
    json.dump(merged_data, f, indent=4)

print(f"合并后的 JSON 文件已保存到: {output_file}")