import json

# 目标函数名列表
functions = [
    "cin", "getenv", "getenv_s", "_wgetenv", "_wgetenv_s", "catgets", "gets", "getchar", "getc", 
    "getch", "getche", "kbhit", "stdin", "getdlgtext", "getpass", "scanf", "fscanf", "vscanf", 
    "vfscanf", "istream.get", "istream.getline", "istream.peek", "istream.read*", "istream.putback", 
    "streambuf.sbumpc", "streambuf.sgetc", "streambuf.sgetn", "streambuf.snextc", "streambuf.sputbackc", 
    "SendMessage", "SendMessageCallback", "SendNotifyMessage", "PostMessage", "PostThreadMessage", 
    "recv", "recvfrom", "Receive", "ReceiveFrom", "ReceiveFromEx", "Socket.Receive*", "memcpy", 
    "wmemcpy", "_memccpy", "memmove", "wmemmove", "memset", "wmemset", "memcmp", "wmemcmp", "memchr", 
    "wmemchr", "strncpy", "_strncpy*", "Istropyn", "_tcsncpy*", "_mbsnbcpy*", "_wesncpy*", "wesncpy", 
    "strncat", "_strncat*", "_mbsncat*", "wesncat*", "bcopy", "strepy", "Istropy", "wescpy", "_tescpy", 
    "_mbscpy", "CopyMemory", "strcat", "Istrcat", "Istrlen", "strchr", "strcmp", "stroll", "strespn", 
    "strerror", "strlen", "strpbrk", "strichr", "strspn", "strstr", "strtok", "strxfrm", "readlink", 
    "fgets", "sscanf", "swscanf", "sscanf_s", "swscanf_s", "printf", "vprintf", "swprintf", "vsprintf", 
    "asprintf", "vasprintf", "fprintf", "sprint", "sprintf", "_sprintf*", "_snwprintf*", "vsnprintf", 
    "CString.Format", "CString.FormatV", "CString.FormatMessage", "CStringT.Format", "CStringT.FormatV", 
    "CStringT.FormatMessage", "CStringT.FormatMessageV", "syslog", "malloc", "Winmain", "GetRawInput*", 
    "GetComboBoxInfo", "GetWindowText", "GetKeyNameText", "Dde*", "GetFileMUI*", "GetLocaleInfo*", 
    "GetString*", "GetCursor*", "GetScroll*", "GetDIgItem*", "GetMenultem*", "free", "delete", "new", 
    "malloc", "realloc", "calloc", "_alloca", "strdup", "asprintf", "vsprintf", "vasprintf", "sprintf", 
    "_sprintf", "_snwprintf", "vsnprintf"
]

def contains_functions(code):
    """检查code中是否包含任意函数名"""
    for function in functions:
        if function in code:
            return True
    return False

def filter_samples_with_functions(json_file, output_file):
    """只保留包含目标函数的样本并保存到新JSON文件"""
    with open(json_file, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 只保留包含目标函数的样本
    filtered_samples = [sample for sample in data if 'code' in sample and contains_functions(sample['code'])]
    
    # 将结果保存到新JSON文件
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump(filtered_samples, outfile, indent=4, ensure_ascii=False)

    print(f'包含目标函数的样本数量: {len(filtered_samples)}')

# 使用示例
json_file_path = 'path'
output_file_path = 'Reveal_non_vul_func.json'
filter_samples_with_functions(json_file_path, output_file_path)
