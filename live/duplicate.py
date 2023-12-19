#!/bin/python3

import sys
import os  
import hashlib  

# 将一个文件中所有重复的行删除,顺序打乱
def file_duplicate(filename):

    print("start file_duplicate: " + filename)

    # 打开输入文件  
    with open(filename, 'r') as input_file:
        # 创建一个哈希表来存储行  
        lines_set = set()  
        # 创建一个列表来存储唯一的行  
        lines_list = []  
        # 遍历每一行  
        for line in input_file:  
            # 使用哈希值作为行的唯一标识符  
            line_hash = hashlib.sha256(line.encode('utf-8')).hexdigest()  
            # 如果行不在哈希表中，则将其添加到哈希表和列表中  
            if line_hash not in lines_set:  
                lines_set.add(line_hash)  
                lines_list.append(line)  

        # 将唯一的行写入输出文件  
        with open(filename + '.1', 'w') as output_file:  
            output_file.writelines(lines_list)

    os.rename(filename + '.1', filename)

def file_replace(filename, oldstr, newstr):
    # 打开文件  
    with open(filename, 'r') as file:  
        # 读取文件内容  
        content = file.read()  
    # 替换字符串  
    new_content = content.replace(oldstr, newstr)  
    # 写入文件  
    with open(filename + '.1', 'w') as file:  
        # 写入新的内容  
        file.write(new_content)
    os.rename(filename + '.1', filename)

# 使用func函数依次对某个目录下的所有文件进行操作
def dir_doing(dir_path, func):  
    for root, dirs, files in os.walk(dir_path):  
        for file in files:  
            filename = os.path.join(root, file)
            func(filename) 
        if dirs:
            for subdir in dirs:  
                dir_doing(os.path.join(root, subdir), func) 

def file_doing(filename, func):  
    isDir = os.path.isdir(filename)
    if isDir:
        dir_doing(filename, func)
    else:
        func(filename)



###################################################
def m3u_duplicate(filename):  
    file_replace(filename, "\r", "\n")
    file_replace(filename, "\n\n", "\n")
    file_replace(filename, "\nhttp", ",http")
    file_duplicate(filename)
    file_replace(filename, ",http", "\nhttp")

def string_list_sort(str_list):  
    chinese_list = []  
    english_list = []  
    
    for item in str_list:
        if item.isalpha():  
            english_list.append(item)  
        else:  
            chinese_list.append(item)

    english_list.sort()
    chinese_list.sort()
    return english_list + chinese_list


def txt_group_sort(filename):  

    print("start txt_group_sort: " + filename)

    file_replace(filename, "\r", "\n")
    file_replace(filename, "\n\n", "\n")

    # 打开输入文件  
    with open(filename, 'r') as input_file:

        with open(filename + '.1', 'w') as output_file:  
            lines_list = []  
            # 遍历每一行  
            for line in input_file:  
                # 如果是group, 
                if "#genre#" in line: # groupname
                    #先对原有的列表排序写到另一个文件,再清空
                    if lines_list:
                        lines_list = string_list_sort(lines_list)
                        output_file.writelines(lines_list)
                        lines_list = []

                    #然后直接将tittle写到另一个文件
                    output_file.write("\n" + line)
                    continue

                # 如果是普通行, 则加入到列表中                
                if line != '\n':
                    lines_list.append(line)

            #最后一个group
            if lines_list:
                lines_list = string_list_sort(lines_list)
                output_file.writelines(lines_list)

            output_file.write("\n")

    os.rename(filename + '.1', filename)


###################################################
def main():
    args = sys.argv[1:]
    if not args:
        print('usage: python3 %s file'% sys.argv[0])
        sys.exit(1)

    filename = args[0]
    file_doing(filename, file_duplicate)
    print("去重完成")

###################################################
if __name__ == '__main__':
    # main()

    file_doing("./m3u", m3u_duplicate)

    file_doing("./txt", file_duplicate)
    file_doing("./txt", txt_group_sort)

    
