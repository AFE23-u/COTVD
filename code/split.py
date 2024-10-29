import json
import random

# 加载JSON数据
def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# 保存JSON数据
def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# 按照label将数据分开
def split_by_label(data):
    label_0 = [sample for sample in data if sample['label'] == 0]
    label_1 = [sample for sample in data if sample['label'] == 1]
    return label_0, label_1

# 按照8:1:1比例划分数据
def split_data(data, train_ratio=0.8, valid_ratio=0.1):
    random.shuffle(data)
    train_end = int(train_ratio * len(data))
    valid_end = int((train_ratio + valid_ratio) * len(data))
    train_data = data[:train_end]
    valid_data = data[train_end:valid_end]
    test_data = data[valid_end:]
    return train_data, valid_data, test_data

# 统计样本数量
def count_labels(data):
    count_0 = sum(1 for sample in data if sample['label'] == 0)
    count_1 = sum(1 for sample in data if sample['label'] == 1)
    return count_0, count_1

# 主函数
def main(input_file):
    # 加载数据
    data = load_json(input_file)
    
    # 按照label分开
    label_0, label_1 = split_by_label(data)
    
    # 分别划分0类和1类数据
    train_0, valid_0, test_0 = split_data(label_0)
    train_1, valid_1, test_1 = split_data(label_1)
    
    # 合并0类和1类数据
    train_data = train_0 + train_1
    valid_data = valid_0 + valid_1
    test_data = test_0 + test_1
    
    # 保存划分后的数据集
    save_json(train_data, 'train.json')
    save_json(valid_data, 'valid.json')
    save_json(test_data, 'test.json')
    
    # 统计并输出样本信息
    train_0_count, train_1_count = count_labels(train_data)
    valid_0_count, valid_1_count = count_labels(valid_data)
    test_0_count, test_1_count = count_labels(test_data)

    print(f"Train set: 0-label: {train_0_count}, 1-label: {train_1_count}, Total: {len(train_data)}")
    print(f"Valid set: 0-label: {valid_0_count}, 1-label: {valid_1_count}, Total: {len(valid_data)}")
    print(f"Test set: 0-label: {test_0_count}, 1-label: {test_1_count}, Total: {len(test_data)}")

if __name__ == '__main__':
    input_file = 'cotvd.json'  # 替换为你的json文件路径
    main(input_file)
