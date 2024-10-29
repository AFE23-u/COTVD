import subprocess
import os
import json
from output import parse_output
import re


# 定义从文件生成 cpg.bin 的函数
def generate_cpg_bin(source_code_dir, output_dir):
    try:
        # 使用 joern-parse 命令生成 cpg.bin 文件
        command = f'joern-parse {source_code_dir}'
        subprocess.run(command, shell=True, check=True)
        print(f"CPG generated at {output_dir}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during CPG generation: {e.stderr}")
        return False

# 从 JSON 文件中读取代码并保存为 .c 文件，并且只分析出现在代码中的 target 函数
def extract_code_and_analyze(json_file, joern_script_path, target_list, out_file, log_location):
    # 编译正则表达式以精确匹配目标函数
    target_patterns = [re.compile(rf'\b{re.escape(target)}\b') for target in target_list if target]

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 遍历 JSON 文件中的每个代码块
    for idx, entry in enumerate(data):
        # todo 重设idx 如果中途失败，找到log_locaiton.txt中最后打印的一个，替换下面的索引即可
        if idx < 7738:
            continue
        # 记录 idx, 打印出来的idx表示其上一个没有问ix题，应该从当前这个开始
        with open(log_location, 'a', encoding='utf-8') as f:   
                f.write(str(idx) + '\n')
                f.close
        # todo 原json文件中源代码的键名
        code_block = entry.get("func", "")
        if not code_block:
            print(f"Skipping entry {idx} due to missing code.")
            continue
        
        # 根据代码块内容过滤 target_list，只保留实际出现在代码中的函数
        filtered_targets = [target for target, pattern in zip(target_list, target_patterns) if pattern.search(code_block)]
        if not filtered_targets:
            print(f"No targets found in entry {idx}, skipping.")
            with open(log_location, 'a', encoding='utf-8') as f:   
                f.write('无目标函数\n')
                f.close
            continue
        
        print(f"Targets found in entry {idx}: {filtered_targets}")

        # 在执行目录下创建 .c 文件
        c_file_path = f"temp_code_{idx}.c"
        
        # 将 code 写入 .c 文件
        with open(c_file_path, 'w', encoding='utf-8') as f:
            f.write(code_block)
        
        print(f"C file created for entry {idx}: {c_file_path}")

        # 生成 cpg.bin 文件
        output_cpg_bin = f"cpg.bin"
        if generate_cpg_bin(c_file_path, os.path.dirname(output_cpg_bin)):
            # 确认生成的 cpg.bin 存在
            if os.path.exists(output_cpg_bin):
                # 将过滤后的 target 列表转换为逗号分隔的字符串
                targets_str = ",".join(filtered_targets)
                
                # 构建调用 joern.sc 的 shell 命令
                command = f'joern --script {joern_script_path} --param cpgFile="{output_cpg_bin}" --param targetStr="{targets_str}" --param outFile="{out_file}"'

                # 执行 shell 命令
                try:
                    result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
                    print(f"Shell script executed successfully for entry {idx}.")
                    print("Output:", result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"Error occurred for entry {idx}: {e.stderr}")
            else:
                print(f"Error: The CPG file {output_cpg_bin} was not found for entry {idx}.")
        
        
        # 处理output.txt
        parsed_data = parse_output(out_file)
        with open(c_file_path, 'r') as f:
            source_c = f.readlines()
            
        # 替换c_file_path中的内容
        for key, indices in parsed_data.items():
            parsed_data[key] = [(i, source_c[i-1]) for i in indices]
            
        data[idx]['slice'] = parsed_data        
        
        # 删除 .c 文件
        os.remove(c_file_path)
        print(f"C file deleted for entry {idx}: {c_file_path}")
        
        # 每过一个idx，保存一次新json
        with open(json_file, 'w', encoding='utf-8') as f:   
                json.dump(data, f, ensure_ascii=False, indent=4)
    print('Finished!')
            
# 设置路径和参数
# todo json_file 处理过后，带有目标函数切片的会在原json上多一个"slice"键值对，需要新开一个脚本将没有result的样本去掉
json_file = "Devign_func.json"  # JSON 文件路径

joern_script_path = "COTVD/code/joern.sc"  # joern.sc 脚本路径
target_list = ["cin","getenv","getenv_s","_wgetenv","_wgetenv_s","catgets","gets","getchar","getc","getch","getche","kbhit","stdin","getdlgtext","getpass","scanf","fscanf","vscanf","vfscanf","istream.get","istream.getline","istream.peek","istream.read*","istream.putback","streambuf.sbumpc","streambuf.sgetc","streambuf.sgetn","streambuf.snextc","streambuf.sputbackc","SendMessage","SendMessageCallback","SendNotifyMessage","PostMessage","PostThreadMessage","recv","recvfrom","Receive","ReceiveFrom","ReceiveFromEx","Socket.Receive*","memcpy","wmemcpy","_memccpy","memmove","wmemmove","memset","wmemset","memcmp","wmemcmp","memchr","wmemchr","strncpy","_strncpy*","Istropyn","_tcsncpy*","_mbsnbcpy*","_wesncpy*","wesncpy","strncat","_strncat*","_mbsncat*","wesncat*","bcopy","strepy","Istropy","wescpy","_tescpy","_mbscpy","CopyMemory","strcat","Istrcat","Istrlen","strchr","strcmp","stroll","strespn","strerror","strlen","strpbrk","strichr","strspn","strstr","strtok","strxfrm","readlink","fgets","sscanf","swscanf","sscanf_s","swscanf_s","printf","vprintf","swprintf","vsprintf","asprintf","vasprintf","fprintf","sprint","sprintf","_sprintf*","_snwprintf*","vsnprintf","CString.Format","CString.FormatV","CString.FormatMessage","CStringT.Format","CStringT.FormatV","CStringT.FormatMessage","CStringT.FormatMessageV","syslog","malloc","Winmain","GetRawInput*","GetComboBoxInfo","GetWindowText","GetKeyNameText","Dde*","GetFileMUI*","GetLocaleInfo*","GetString* GetCursor* ","GetScroll*","GetDIgItem*","GetMenultem*","free","delete","new","malloc","realloc","calloc","_alloca","strdup","asprintf","vsprintf","vasprintf","sprintf","sprintf","_sprintf","_snwprintf","vsnprintf"]  # 目标函数的列表
out_file = "output.txt"  # 合并输出文件路径
log_location = "log_location.txt"

# 从 JSON 文件中提取所有代码块，并执行分析
extract_code_and_analyze(json_file, joern_script_path, target_list, out_file, log_location)
