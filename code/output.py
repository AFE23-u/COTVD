import re

def parse_output(output_text):
    with open(output_text) as file:
        output_text = file.read()

    # 初始化结果字典
    result = {}
    
    # 提取target和对应的内容
    targets = re.findall(r'Results for target: (\w+)', output_text)
    graphs = re.split(r'Results for target: \w+', output_text)[1:]
    # 将每个graph中的换行符切分成单独的行
    graphs = [g.split('\n') for g in graphs]

    # 遍历targets和对应的graphs
    for i, target in enumerate(targets):
        # 找到target对应的id
        target_list = []
        pattern = rf'\b{re.escape(target)}\b'  # 预编译正则表达式

        for g in graphs[i]:
            if '" -> "' in g:  # 用'in'替换__contains__，更简洁
                break
            if re.search(pattern, g) and re.search(r'"\d+"', g):
                target_list.append(g)
    
        target_list = [re.search(r'"\d+"', x).group(0).strip('"') for x in target_list]
        # 找到与id有关联的id
        target_related_ids = set()
        for g in graphs[i]:
            if '" -> "' in g: 
                for t_id in target_list:
                    if str(t_id) in g:
                        # 使用正则表达式匹配两组数字
                        matches = re.findall(r'"\d+"', g)
                        # 去除引号并将结果存入列表
                        temp_r = [match.strip('"') for match in matches]
                        target_related_ids.update(temp_r)               
                        
        # 提取行号
        line_nums = set()
        for g in graphs[i]:
            if '" -> "' not in g: 
                for id in target_related_ids:
                    if str(id) in g:
                        matches = re.findall(r'<SUB>(\d+)</SUB>', g)
                        line_nums.update(matches)
        # 添加到result
        result[target] = sorted([int(i) for i in line_nums])
        
    temp_set = set()
    for v in result.values():
        temp_set.update(v)
        
    result['result'] = sorted([int(i) for i in temp_set])
    return result


# parsed_data = parse_output(output_text)


