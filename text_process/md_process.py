#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import datetime
import shutil


def rename_files_end(path, old_extension, new_extension, file_remove_length=0, dir_remove_length=0):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(old_extension):
                os.rename(os.path.join(root, file),
                          os.path.join(root, file[:-(len(old_extension)+file_remove_length)]+new_extension))
        for dir in dirs:
            if dir_remove_length > 0:
                os.rename(os.path.join(root, dir), os.path.join(
                    root, dir[:-(dir_remove_length)]))


def rename_files(path, replace_list):
    for root, dirs, files in os.walk(path):
        for file in files:
            file_old = file
            for replace_str in replace_list:
                if file.find(replace_str[0]) != -1:
                    file = file.replace(replace_str[0], replace_str[1])
            os.rename(os.path.join(root, file_old),
                      os.path.join(root, file))
        for dir in dirs:
            dir_old = dir
            for replace_str in replace_list:
                if dir.find(replace_str[0]) != -1:
                    dir = dir.replace(replace_str[0], replace_str[1])
            os.rename(os.path.join(root, dir_old),
                      os.path.join(root, dir))

# remove line with search_str


def remove_line(path, search_list):
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.md'):
                with open(os.path.join(root, file), 'r', encoding='UTF-8') as f:
                    lines = f.readlines()
                with open(os.path.join(root, file), 'w', encoding='UTF-8') as f:
                    for l in lines:
                        flag = 0
                        for search_str in search_list:
                            if l.find(search_str) != -1:
                                flag = flag+1
                        if flag == 0:
                            f.write(l)


def mulu_process(replace_list):
    with open("目录.md", 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    with open("目录.md", 'w', encoding='UTF-8') as f:
        for l in lines:
            for replace_str in replace_list:
                if l.find(replace_str[0]) != -1:
                    l = l.replace(replace_str[0], replace_str[1])
            f.write(l)


def num2str_title(num):
    if num < 10:
        return '00'+str(num)
    elif num < 100:
        return '0'+str(num)
    else:
        return str(num)


def search_file(path):
    with (open("目录.md", 'r', encoding='UTF-8')) as f:
        lines = f.readlines()
        for root, dirs, files in os.walk(path):
            counter = 0
            for line in lines:
                if line[:-1]+'.md' in files:
                    counter = counter+1
                    os.rename(os.path.join(
                        root, line[:-1]+'.md'), os.path.join(root, num2str_title(counter)+line[:-1]+'.md'))
                    print(line[:-1]+'.md')


def global_replace_list():
    global replace_list
    replace_list = [["「", "_"], ["」", "_"], [
        "，", ","], ["：", "_"], [" ", "_"], ["“", "_"], ["”", "_"], ["？", "?"], ["·", "_"]]


def remove_line_test1():
    path = os.getcwd()
    search_list = ["- created: 2022", "- source: https://www.zhihu.com"]
    remove_line(path, search_list)


def rename_files_end_test1():
    path = os.getcwd()
    rename_files_end(path, '.md', '.md', 1, 1)


def replace_name_test1():
    path = os.getcwd()
    global_replace_list()
    rename_files(path, replace_list)


def tianjiaxiahuaxian():
    for root, dirs, files in os.walk("."):
        for i in range(1, 38):
            for file in files:
                if file[:3] == num2str_title(i):
                    print(file)


def back_up_dir(path):

    time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # get the father path
    father_path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
    # get current dir name
    dir_name = os.path.basename(path)
    back_path = os.path.join(father_path, dir_name+"_"+time_str)
    # os.mkdir(back_path)
    # copy all files in the current path to the back_path
    shutil.copytree(path, back_path)


if __name__ == '__main__':
    path = os.getcwd()
    # search_file(path)
    # global_replace_list()
    # mulu_process(replace_list)

    back_up_dir(path)
