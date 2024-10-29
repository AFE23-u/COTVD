import json
import torch
import numpy as np
import os


# 提取危险函数及其依赖
def extract_dangerous_function_slice(sample):
    dangerous_functions = list(sample['slice'].keys())  # 获取危险函数调用
    dependencies = sample['slice']['result']  # 获取相关依赖
    return dangerous_functions, '\n'.join(['<'+str(x[0])+'> '+x[1].replace('\n','').strip() for x in dependencies])

# 将代码中的换行符替换为行号 token，并去除每行开头和结尾的多余空格
def add_line_tokens_to_code(code):
    lines = code.split('\n')  # 按行分割代码
    tokenized_lines = [f"<{i+1}> {line.strip()}" for i, line in enumerate(lines)]  # 去掉每行多余的空格并为每一行添加行号 token
    return '\n'.join(tokenized_lines)  # 将处理后的代码重新合并为字符串

# 生成包含格式化标签要求的 prompt
def generate_prompt_with_label(sample):
    code = add_line_tokens_to_code(sample['code'])  # 对代码添加行号 token
    label = sample['label']
    dangerous_functions, dependencies = extract_dangerous_function_slice(sample)
    
    # 合并所有危险函数调用
    func_list = ', '.join(dangerous_functions)
    
    # 提取数据依赖和控制依赖并合并，使用行号 token
    combined_dependencies = dependencies
    example_zero = None
    example_one = None    
    
    # todo 生成 prompt, 在notion中找到prompt替换。
    prompt = f"""{combined_dependencies}"""
    
    return [(prompt, label)]

# 批量处理数据集并生成 prompt
def process_dataset(dataset):
    all_prompts = []
    for sample in dataset:
        prompts = generate_prompt_with_label(sample)
        all_prompts.extend(prompts)
    return all_prompts

# 从JSON文件中读取数据集
def load_dataset_from_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        dataset = json.load(file)
    return dataset


# 将 prompt 输出到文件
def save_prompts_to_file(prompts, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        for prompt in prompts:
            if prompt[1] ==1:
                file.write(prompt[0].replace('\n', '\\n') + '\n')  # 保留 \n 而不是换行符

# 主函数
if __name__ == "__main__":
    # todo
    json_file = "train.json"  # 替换为您的JSON文件路径
    output_file = "train_1_slice.txt"  # 输出的prompt文件
    
    # 从 JSON 文件中加载数据集
    dataset = load_dataset_from_json(json_file)
    
    # 处理数据集并生成 prompts
    prompts = process_dataset(dataset)
    
    # 将生成的 prompts 保存到文件
    save_prompts_to_file(prompts, output_file)
    
    print(f"Prompts have been generated and saved to {output_file}.")
