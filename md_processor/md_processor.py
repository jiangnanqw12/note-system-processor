#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import time

import os
import datetime
import shutil
import argparse
import aspose.words as aw
import urllib.parse


def back_up_dir_tree(path):

    time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # get the father path
    father_path = os.path.abspath(os.path.dirname(path) + os.path.sep + ".")
    # get current dir name
    dir_name = os.path.basename(path)
    back_path = os.path.join(father_path, dir_name+"_"+time_str)
    # os.mkdir(back_path)
    # copy all files in the current path to the back_path
    shutil.copytree(path, back_path)


def back_up_dir(src_dir):

    time_str = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # get the father path
    father_path = os.path.abspath(os.path.dirname(src_dir) + os.path.sep + ".")
    # get current dir name
    dir_name = os.path.basename(src_dir)
    back_path = os.path.join(src_dir, dir_name+"_"+time_str)
    # os.mkdir(back_path)
    if not os.path.exists(back_path):
        os.makedirs(back_path)
    # copy all files in the current path to the back_path
    for filename in os.listdir(src_dir):
        src_path = os.path.join(src_dir, filename)
        dst_path = os.path.join(back_path, filename)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)


def num2str_title(num):
    return str(num).zfill(3)


def rename_files_base_on_index_markdown(path=None):
    counter = 0
    if path is None:
        path = os.getcwd()
    with open(os.path.join(path, "000_index.md"), 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    files = os.listdir(path)
    for i, line in enumerate(lines):
        line = line.strip().replace("%", "_")
        note_name = line + '.md'
        if note_name in files:
            counter += 1
            os.replace(os.path.join(path, note_name),
                       os.path.join(path, num2str_title(counter) + "_" + note_name))
        else:
            print(files)
            raise FileNotFoundError(f"{note_name} not in the files list")


def add_timestamp_to_filenames():
    current_dir = os.getcwd()
    timestamp = int(time.time())
    for filename in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, filename)) and not filename.endswith(".py"):
            filename_without_ext, ext = os.path.splitext(filename)
            new_filename = f"{filename_without_ext}_{timestamp}{ext}"
            os.replace(os.path.join(current_dir, filename),
                       os.path.join(current_dir, new_filename))


def text_replace(root_dir: str, replace_list: list):
    assets_root_path, assets_root_dir = get_assets_root_path()
    output_dir = create_output_directory(assets_root_path)
    for filename_with_ext in os.listdir(root_dir):
        if filename_with_ext.endswith('.md'):
            src_path = os.path.join(root_dir, filename_with_ext)
            dest_path = os.path.join(output_dir, filename_with_ext)

            with open(src_path, 'r', encoding='UTF-8') as f_src, open(dest_path, 'w', encoding='UTF-8') as f_dest:
                for line in f_src:
                    for replace_item in replace_list:
                        line = line.replace(replace_item[0], replace_item[1])
                    f_dest.write(line)


def mdx2md(timestamp: int = 1676880280):
    assets_root_path, assets_root_dir = get_assets_root_path()
    output_dir = create_output_directory(assets_root_path)
    cwd = os.getcwd()
    # text_replace_list_mdx2md3 = [
    #                              ]
    # replace_list = text_replace_list_mdx2md3
    # <Figure
    for filename_with_ext in os.listdir(cwd):
        if filename_with_ext.endswith('.md'):
            src_path = os.path.join(cwd, filename_with_ext)
            dest_path = os.path.join(output_dir, filename_with_ext)

            # with open(src_path, 'r', encoding='UTF-8') as f_src, open(dest_path, 'w', encoding='UTF-8') as f_dest:
            #     for line in f_src:
            #         for replace_item in replace_list:
            #             line = line.replace(replace_item[0], replace_item[1])
            #         f_dest.write(line)
            with open(src_path, 'r', encoding='UTF-8') as f_src:
                content = f_src.read()
            # Define the regex pattern and replacement string

            replace_list_regex = [
                                 [r"<PiCreature\n{0,}\s{0,}(.+)\n{0,}\s{0,}(.+)\n{0,}\s{0,}/>", r"\1\n\2\n"],
                # [r"show=\"video\"\n", r""],
                #  [r"<!--", r""],
                #  [r"-->", r""],
                                 [r"<Question", r"---"],
                                 [r"<FreeResponse>", r"---"],
                [r"</FreeResponse>", r"---"],
                [r"</Question>", r"---"],
                [r'''<Figure[\n ]{1,}image="(.+)(\.svg|\.png|\.jpg)"[\w ._="'\n_%]{0,}/>''',
                                     r'![](\1_'+str(timestamp)+r'\2)'],
                [r'<Accordion\stitle=".+">\n', r''],
                [r'</Accordion>\n', r''],
                # [r'emotion="\w+"[ \t]+\n', r''],
                # [r'flip=\{(true|false)\}\n', r''],
                # [r'(?s)<Question .+?</Question>', r'tttttttttttttttttttt'],
                [r'answer=\{(\d)\}[ \n\t]{0,}>',
                                     r'\n<details><summary>answer</summary><p>Choice= \1</p></details>\n\n- **Explanation**'],
                # [r'''<Question[\n \t]{0,}question="(.+)"[\n \t]{0,}choice1="(.+)"[\n \t]{0,}choice2="(.+)"[\n \t]{0,}choice3="(.+)"[\n \t]{0,}choice4="(.+)"[\n \t]answer=\{(\d)\}[\n \t]{0,}>''',r'- **Question**\n\t\1']
                [r'[ \t]{0,}question="(.+)"',
                                     r'- **Question**\n\t\1'],
                [r'[ \t]{0,}choice1="(.+)"',
                                     r'    - **Choice 1=** \1'],
                [r'[ \t]{0,}choice2="(.+)"',
                                     r'    - **Choice 2=** \1'],
                [r'[ \t]{0,}choice3="(.+)"', r'    - **Choice 3=** \1'],
                [r'[ \t]{0,}choice4="(.+)"', r'    - **Choice 4=** \1'],
                # [r'video=".+\.mp4"', r''],
                # [r'show="video"', r''],
                [r'([ \t]{0,}\n){3,}', r'\1\1'],
                # ['/>', r''],
            ]

            for i in range(len(replace_list_regex)):
                pattern = replace_list_regex[i][0]
                replacement = replace_list_regex[i][1]

                # Perform the regex replacement
                content = re.sub(pattern, replacement, content)
            # Write the modified content to the output Markdown file with UTF-8 encoding
            with open(dest_path, 'w', encoding='utf-8') as file:
                file.write(content)


def copy_timestamps_and_index_2_root(directory=None):
    """
    Copies files with 'timestamps' in their name and '.mdx' extension to the root directory
    with an updated name. Also copies files with 'index' in their name and '.mdx' extension
    to the root directory with an updated name.
    """
    if directory is None:
        directory = os.getcwd()

    current_folder_name = os.path.basename(directory)
    filelist = os.listdir(directory)

    for file in filelist:
        file_name, file_extension = os.path.splitext(file)

        if "timestamps" in file_name and file_extension == '.md':
            new_file_name1 = f"timestamps_{current_folder_name}.md"
            dest_path1 = os.path.join(directory, '../..', new_file_name1)

            if not os.path.exists(dest_path1):
                shutil.copy(file, dest_path1)

        if file_extension == '.mdx':
            if "index" in file_name:
                new_file_name = f"{current_folder_name}.md"
                dest_path = os.path.join(directory, '../..', new_file_name)

                if not os.path.exists(dest_path):
                    shutil.copy(file, dest_path)


def get_father_path(path):
    return os.path.dirname(path)


# 0


def convert_subtitle_chatgpt_summary_to_markdown_vid_timeline(str_url):

    # str_url=r'![009_area-and-slope.mp4](file:///C:%5CBaiduSyncdisk%5Cassets%5CO%5CO1%5CO17%5CO172%5CCalculus%203Blue1Brown%5Cassets%5Cbvids%5C009_area-and-slope.mp4)'

    match1 = check_video_file_path_conforms_to_pattern(str_url)
    cwd = os.getcwd()
    file_list = os.listdir(cwd)
    assets_root_path, assets_root_dir = get_assets_root_path()
    create_output_directory(assets_root_path)

    for file in file_list:
        if file.endswith(".md"):
            if file.find("summary_gpt") != -1:
                key_word = "summary_gpt"
                list_time_head_textshort_text = get_list_time_head_textshort_text_4_file(
                    file, key_word)
                list_time_head_textshort_text_to_vid_timeline_md(
                    list_time_head_textshort_text, file, match1)


def merge_list_time_head_textshort_text(list_time_text, list_time_head_textshort):
    # print("list_time_head_textshort is :")
    # print(list_time_head_textshort)
    # print("list_time_text is :")
    # print(list_time_text)

    for i in range(len(list_time_head_textshort)):
        # print(list_time_head_textshort[i][0])
        for j in range(len(list_time_text)):
            if list_time_head_textshort[i][0] == list_time_text[j][0]:

                time_text = list_time_text.pop(j)
                print(time_text)
                list_time_head_textshort[i][3] = time_text[3]
                # list_time_head_textshort.append([list_time_head_textshort[i][0],list_time_head_textshort[i][1],list_time_head_textshort[i][2],time_text[3]])
                break
    # print("first merge list_time_head_textshort_text is :")
    # print(list_time_head_textshort)
    list_time_head_textshort_text = list_time_head_textshort
    if len(list_time_text) > 0:
        # print("remain:",list_time_text)

        list_pop = []
        for i in range(len(list_time_text)):
            for j in range(len(list_time_head_textshort_text)):
                time_text = int(list_time_text[i][0])
                time_shorttext = int(list_time_head_textshort_text[j][0])
                if j != len(list_time_head_textshort_text)-1:
                    time_shorttext_next = int(
                        list_time_head_textshort_text[j+1][0])

                    if time_text > time_shorttext and time_text < time_shorttext_next:

                        list_time_head_textshort_text.insert(
                            j+1, [list_time_text[i][0], None, None, list_time_text[i][3]])
                        list_pop.append(list_time_text[i])
                        break
                else:
                    if time_text > time_shorttext:
                        list_time_head_textshort_text.append(
                            [list_time_text[i][0], None, None, list_time_text[i][3]])
                        list_pop.append(list_time_text[i])
                        break
        for elment in list_pop:
            index = list_time_text.index(elment)
            list_time_text.pop(index)
    if len(list_time_text) > 0:
        print("remain:", list_time_text)

    return list_time_head_textshort_text


def convert_subtitle_and_summary_to_markdown_vid_timeline(str_url):

    # str_url=r'![009_area-and-slope.mp4](file:///C:%5CBaiduSyncdisk%5Cassets%5CO%5CO1%5CO17%5CO172%5CCalculus%203Blue1Brown%5Cassets%5Cbvids%5C009_area-and-slope.mp4)'

    match1 = check_video_file_path_conforms_to_pattern(str_url)
    cwd = os.getcwd()
    file_list = os.listdir(cwd)
    assets_root_path, assets_root_dir = get_assets_root_path()
    output_dir = create_output_directory(assets_root_path)

    for file in file_list:
        if file.endswith(".md"):
            if file.find("subtitle") != -1:
                key_word = "subtitle"
                list_time_text = get_list_time_head_textshort_text_4_file(
                    file, key_word)
                # list_time_head_textshort_text_to_vid_timeline_md(list_time_head_textshort_text,file,match1)

            if file.find("summary_gpt") != -1:
                cwd_floder_name = os.path.basename(cwd)
                file_summary = file
                key_word = "summary_gpt"
                list_time_head_textshort = get_list_time_head_textshort_text_4_file(
                    file, key_word)
                # list_time_head_textshort_text_to_vid_timeline_md(list_time_head_textshort_text,file,match1)

    list_time_head_textshort_text = merge_list_time_head_textshort_text(
        list_time_text, list_time_head_textshort)
    print("final is:")
    print(list_time_head_textshort_text)
    list_time_head_textshort_text_to_vid_timeline_md(
        list_time_head_textshort_text, file_summary, match1)
    convert_md_vid_link_to_html(output_dir)
    return output_dir, file_summary


def get_current_timestamp():
    timestamp = int(time.time())
    print(timestamp)
    return timestamp


def add_timestamp_to_filenames():
    current_dir = os.getcwd()
    timestamp = int(time.time())
    print("add_timestamp is : ", timestamp)
    for filename in os.listdir(current_dir):
        if os.path.isfile(os.path.join(current_dir, filename)) and not filename.endswith(".py"):
            filename_without_ext, ext = os.path.splitext(filename)
            new_filename = f"{filename_without_ext}_{timestamp}{ext}"
            os.replace(os.path.join(current_dir, filename),
                       os.path.join(current_dir, new_filename))


def create_directory_assets_imgs():
    dirs = [
        "assets/imgs",
        "assets/vids"
    ]

    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")


def create_directory_assets_concept_structure():
    dirs = [
        "assets",
        "assets/imgs",
        "assets/lectures",
        "assets/papers",
        "lectures",
        "papers",
    ]

    for directory in dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")


def open_folder_in_windows(folder_path):
    """Open a folder in Windows File Explorer based on the folder path.

    Args:
    folder_path (str): The folder path to open.

    Returns:
    None
    """
    if os.path.exists(folder_path):
        os.startfile(folder_path)
    else:
        print(f"Folder path {folder_path} does not exist.")


def open_b_assets_folder(cwd=None):
    if cwd is None:
        cwd = os.getcwd()
    print(cwd)
    if cwd.find("OneDrive") == -1:
        raise Exception("This script is only for use with OneDrive.")
    assets_path_front = "C:/BaiduSyncdisk/assets"

    # Split the path after 'KG' and replace backslashes with forward slashes
    kg_path_back = cwd.split("\\KG")[1].replace("\\", "/")

    # Remove the leading forward slash from kg_path_back
    kg_path_back = kg_path_back.lstrip("/")

    assets_path = os.path.join(assets_path_front, kg_path_back)
    if assets_path.find("BaiduSyncdisk") == -1:
        raise Exception("The assets path is not in BaiduSyncdisk.")
    open_folder_in_windows(assets_path)


def html2md(path=None, output_root="C://Output//", output_folder_name=None):
    if path is None:
        path = os.getcwd()
    timestamp = int(time.time())
    intput_path = path
    input_floder_name = os.path.basename(intput_path)
    # replace_list_regex2=[[r'Part \d{2}-Module \d{2}-Lesson (\d{2})_(.+)',r'0\1_\2'],]
    input_floder_name = re.sub(
        r'Part \d{2}-Module \d{2}-Lesson (\d{2})_(.+)', r'0\1_\2', input_floder_name)
    # Part 01-Module 01-Lesson 01_Welcome to the C++ Developer Nanodegree Program
    input_floder_name = input_floder_name.replace(" ", "_")
    output_path = os.path.join(
        output_root, output_folder_name, input_floder_name)
    os.makedirs(output_path, exist_ok=True)

    listfiles = os.listdir(intput_path)
    mp4_list = [
        filename for filename in listfiles if filename.endswith(".mp4")]
    # print(listfiles)
    for i in range(len(listfiles)):
        filename = listfiles[i]  # get all file list
        if filename.endswith(".html"):
            input_file = os.path.join(intput_path, filename)
            doc = aw.Document(input_file)
            output_file = os.path.join(
                output_path, filename.replace(".html", ".md"))
            # print(output_path)

            doc.save(output_file)

    output_files_list = os.listdir(output_path)
    replace_list_regex = [[r'!\[\]\(.+\.001\.png\)', r''],
                          [r'(!\[\]|!\[.+\])(\(.+)(\.png|\.jpg|\.gif|\.jpeg|\.svg|\.wbem)\)',
                              r'\1\2'+f'_{timestamp}'+r'\3)'],
                          [r'\*\*Evaluation Only\. Created with Aspose\.Words\. Copyright 2003-2023 Aspose Pty Ltd\.\*\*', r''],
                          [r'\*\*Created with an evaluation copy of Aspose.Words. To discover the full versions of our APIs please visit: https://products.aspose.com/words/\*\*', r''],
                          [r'\[udacimak v1.4.1\]\(https://github.com/udacimak/udacimak#readme\)', r''],
                          [r'\[.+\]\(.+\.html\)', r''],
                          [r'\n{3,}', r'\n\n'],
                          [r'`[ ]+`', r'    '],
                          ]
    for i in range(len(output_files_list)):
        filename = output_files_list[i]
        if filename.endswith(".001.png"):
            os.remove(os.path.join(output_path, filename))
            continue
        if filename.endswith(".md"):
            if filename == "index.md":
                os.remove(os.path.join(output_path, filename))
                continue
            with open(os.path.join(output_path, filename), 'r', encoding='UTF-8') as f:
                content = f.read()
            with open(os.path.join(output_path, filename), 'w', encoding='UTF-8') as f:

                for replace_list in replace_list_regex:
                    content = re.sub(replace_list[0], replace_list[1], content)
                # f.write(content)

                lines = content.splitlines()
                for line in lines:
                    if len(line) > 4:
                        for file_mp4 in mp4_list:
                            word_list = line.split(" ")
                            flag = 0
                            flag_out = 0
                            for word in word_list:
                                if file_mp4.find(word) > -1:
                                    flag = flag+1
                                elif file_mp4.find(word) == -1:
                                    flag_out = flag_out+1
                            if flag:
                                if flag_out:
                                    # print(line)
                                    pass
                                else:
                                    path_mp4 = os.path.join(
                                        intput_path, file_mp4)
                                    url_path = urllib.parse.quote(
                                        os.path.abspath(path_mp4))
                                    url = "file:///" + \
                                        url_path.replace("\\", "/")
                                    line = line+"\n\n" + \
                                        f"[{file_mp4}]({url})\n" + \
                                        f"![{file_mp4}]({url})"

                    f.write(line+"\n")
    md_note_process(output_path)
    output_files_list = os.listdir(output_path)

    output_path_md = output_path
    output_path_img = os.path.join(
        output_root, "imgs", output_folder_name, input_floder_name)

    # Create the output directory and its subdirectory if they don't exist
    try:
        os.makedirs(output_path_img, exist_ok=True)
    except FileNotFoundError as e:
        if e.winerror == 206:
            # Shorten the filename and try again
            output_path_img = output_path_img = os.path.join(
                output_path_md, "imgs")
            os.makedirs(output_path_img, exist_ok=True)

        else:
            # If it's not WinError 206, raise the original error
            raise e
    for i in range(len(output_files_list)):
        filename = output_files_list[i]
        if filename.endswith(".md"):
            try:
                os.replace(os.path.join(output_path, filename),
                           os.path.join(output_path_md, filename))
            except FileExistsError:
                os.remove(os.path.join(output_path_md, filename))
                os.replace(os.path.join(output_path, filename),
                           os.path.join(output_path_md, filename))

        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".gif"):
            filename_ext = os.path.splitext(filename)[1]
            filename_without_ext = os.path.splitext(filename)[0]
            filename_img = filename_without_ext+f'_{timestamp}'+filename_ext
            try:
                os.replace(os.path.join(output_path, filename),
                           os.path.join(output_path_img, filename_img))
            except FileExistsError:
                os.remove(os.path.join(output_path_img, filename_img))
                os.replace(os.path.join(output_path, filename),
                           os.path.join(output_path_img, filename_img))
            except FileNotFoundError as e:
                if e.winerror == 3:

                    output_path_img = output_path_img = os.path.join(
                        output_path_md, "imgs")
                    os.makedirs(output_path_img, exist_ok=True)
                    os.replace(os.path.join(output_path, filename),
                               os.path.join(output_path_img, filename_img))
                else:
                    # If it's not WinError 206, raise the original error
                    raise e


def html2md_tree():
    files = [f for f in os.listdir() if os.path.isfile(f)]
    directories = [f for f in os.listdir() if os.path.isdir(f)]
    output_folder_dict = dict()
    for directory in directories:
        search_str = r'Part (\d{2})_(.+)'
        match = re.search(search_str, directory)
        if match:
            output_folder_dict[match.group(
                1)] = '0'+match.group(1)+"_"+match.group(2)
    for directory in directories:
        search_str = r'Part (\d{2})-Module \d{2}-Lesson (\d{2})_(.+)'
        match = re.search(search_str, directory)
        if match:
            output_folder1 = "C:\\Output\\"
            output_folder2 = output_folder_dict[match.group(1)]
            # output_folder=os.path.join(output_folder1,output_folder2)
            input_path = os.path.join(os.getcwd(), directory)
            html2md(input_path, output_folder1, output_folder2)


def get_md_files(directory='.'):
    """Return a sorted list of markdown filenames in a given directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.md')]
    # Extract numeric prefix and sort based on it
    files.sort(key=lambda x: int(re.match(r'(\d{3})_', x).group(
        1)) if re.match(r'(\d{3})_', x) else float('inf'))
    return files


def check_md_files(files):

    # Check if files are in expected order
    for i, filename in enumerate(files):
        expected_prefix = f"{i:03d}_"
        if not filename.startswith(expected_prefix):
            print(
                f"Warning: {filename} does not match expected prefix {expected_prefix}")


def merge_files(filenames, output_filename):
    """Merge the content of a list of files and write to a new file."""
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for fname in filenames:
            try:
                with open(fname, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write('\n')  # add blank lines between files
            except IOError:
                print(f'Error opening file {fname}, skipping.')


def merge_all_md_files_into_one():
    """Merge all markdown files in the current directory into one file."""
    root_path, root_dir = get_assets_root_path()
    output_file = os.path.join(root_path, root_dir+".md")
    md_files = get_md_files()
    check_md_files(md_files)
    merge_files(md_files, output_file)


def Merge_all_md_files_into_one_file_base_on_num_index():
    files = [f for f in os.listdir() if f.endswith('.md')]
    files.sort()
    print(files)
    root_path, root_dir = get_assets_root_path()
    with open(os.path.join(root_path, root_dir+".md"), 'w', encoding='utf-8') as f:
        for file in files:
            with open(file, 'r', encoding='utf-8') as f2:
                content = f2.read()
                f.write(content)
                f.write('\n\n')


def zhi_book_process(num=0):
    operations = {
        1: perform_regex_replacement_on_index_file,

        2: perform_regex_replacement_on_zhi_book_mds_name,
        3: rename_files_base_on_index_markdown,
        4: prepend_filename_as_header_if_chapter_present,
        5: lower_header_level_in_md_files,

        6: remove_md_copy_code,
        7: perform_regex_replacement_on_zhi_mds,
        8: convert_zhi_footnote_to_obsidian,
        10: merge_all_md_files_into_one,
    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError(
            "Invalid operation number. Please choose a number between 0 and 4.")


def test():
    pass


def html2md2():
    import html2markdown
    files = [f for f in os.listdir() if os.path.isfile(f)]
    for file in files:
        if file.endswith(".html"):
            with open(file, 'r', encoding='utf-8') as f:
                html_string = f.read()
            markdown_text = html2markdown.convert(html_string)
            with open(file[:-4] + '.md', 'w', encoding='utf-8') as f:
                f.write(markdown_text)


def get_bvids_destination_short(sub_topic1_to_sub_topicn_folder_list, BaiduSyncdisk_assets_root):
    path_temp = BaiduSyncdisk_assets_root
    for i in range(len(sub_topic1_to_sub_topicn_folder_list)-1):

        folder_temp = sub_topic1_to_sub_topicn_folder_list[i].split('_')[0]
        if folder_temp != "FPCV":
            path_temp = os.path.join(path_temp, folder_temp)
        else:
            path_temp = os.path.join(
                path_temp, sub_topic1_to_sub_topicn_folder_list[i])
        if not os.path.exists(path_temp):
            os.makedirs(path_temp)
    return path_temp


def get_bvids_origin_topic_path(BaiduSyncdisk_assets_root):
    return os.path.join(BaiduSyncdisk_assets_root, "assets", "bvids", "mc_1683793602")


def get_note_name():
    file = os.path.basename(os.getcwd())
    return file+".md"


def get_note_vid_tra_name():
    file = os.path.basename(os.getcwd())
    return file+r'_vid_tra'+".md"


def lower_header_level_in_md_files(path=None):
    if path is None:
        path = os.getcwd()

    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    reg_string_head = re.compile(r"(#{1,6}) (.+)")
    # what is compile
    for file in files_md:
        try:
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                lines = f.readlines()

            processed_lines = []
            for line in lines:
                match = reg_string_head.search(line)
                if match:
                    string_sharp = match.group(1)
                    head_num = string_sharp.count("#")
                    line = reg_string_head.sub(
                        (head_num + 1) * "#" + r" \2", line)
                processed_lines.append(line)

            with open(os.path.join(path, file), "w", encoding="utf-8") as f:
                f.writelines(processed_lines)
        except Exception as e:
            print(f"Failed to process file {file} due to {str(e)}")


def prepend_filename_as_header_if_chapter_present(directory=None):
    reg_string1 = r"\d{3}_(第.{1,2}章.+)"
    reg_string2 = r"\d{3}_(\d{1,2} .+)\.md"

    if directory is None:
        directory = os.getcwd()
    reg_string = reg_string2
    files_md = [f for f in os.listdir(directory) if f.endswith('.md')]
    # Iterate over all files in the directory
    for filename in files_md:
        # If the filename contains 'Chapter'
        match = re.search(reg_string, filename)
        if match:
            chapter_name = match.group(1)
            print(chapter_name)
            # Open the file and read its contents
            with open(os.path.join(directory, filename), 'r', encoding="utf-8") as f:
                content = f.readlines()

            # Prepend the filename as a level 2 header
            content.insert(0, f'## {chapter_name}\n')

            # Write the modified content back to the file
            with open(os.path.join(directory, filename), 'w', encoding="utf-8") as f:
                f.writelines(content)


def remove_md_copy_code(path=None):
    if path is None:
        path = os.getcwd()
    reg_string_copy_code = [r"```\n(.+)Copy code", r"```\1\n"]
    reg_string_list = []
    reg_string_list.append(reg_string_copy_code)

    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    perform_regex_replacement_on_files(reg_string_list, path, files_md)


def perform_regex_replacement_on_index_file(directory_path=None):
    """
    This function checks for the existence of an index file in the given directory
    path and performs a regex replacement on it.
    Args:
        directory_path: Path to the directory to check. Defaults to the current working directory.
    Raises:
        FileNotFoundError: If the index file is not found in the directory.
    """
    if directory_path is None:
        directory_path = os.getcwd()

    index_filename = "000_index.md"

    if index_filename not in os.listdir(directory_path):
        raise FileNotFoundError("Index file not found")

    file_paths = [os.path.join(directory_path, index_filename)]
    regex_patterns = [(r"- \[(.+)\]\(.+\)", r"\1")]

    perform_regex_replacement_on_files(
        regex_patterns, directory_path, file_paths)


def perform_regex_replacement_on_zhi_mds(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []
    reg_index_link = [
        r"-\s+\[.+\]\(https://www.zhihu.com/pub/reader/.+\)\n", r""]
    reg_string_list.extend([reg_index_link])
    reg_zhi_sao_ma = [
        r"扫码下载知乎APP 客户端\n\n!\[\]\(.+sidebar-download-qrcode.wybWudky.png\)\n", r""]
    reg_string_list.extend([reg_zhi_sao_ma])
    reg_Back_matter_template = [r"---\n\n- created:.+\n- source: .+", r""]
    reg_string_list.extend([reg_Back_matter_template])

    perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def convert_zhi_footnote_to_obsidian(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []
    # r"[\[1\]](https://www.zhihu.com/pub/reader/120057501/chapter/1302455544230445056#n1s) 在英语中，发散一词是diffuse。注意focused（专注）一词的词尾是-ed，而diffuse则不是。发散一词的意思是“薄薄地弥漫出去”。"
    reg_string1 = [
        r'<sup><a href="https://www\.zhihu\.com/pub/reader.+n\d{1,2}" id="n\d{1,2}s">\[(\d{1,2})\]</a></sup>', r"[^\1]"]
    # r'<sup><a href="https://www\.zhihu\.com/pub/reader.+n\d{1,2}" id="n\d{1,2}s">\[\d{1,2}\]</a></sup>'
    reg_string_list.extend([reg_string1])
    reg_string2 = [
        r'\[\\\[(\d{1,2})\\\]\]\(https://www\.zhihu\.com/pub/.+\) (.+)', r"[^\1]: (\2)"]
    reg_string_list.extend([reg_string2])

    perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def perform_regex_replacement_on_zhi_book_mds_name(path=None):
    if path is None:
        path = os.getcwd()
    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    reg_string_dir = [r"(.+) - .+ - 知乎书店", r"\1"]
    reg_string_md = [r"(.+) - .+ - 知乎书店(\.md)", r"\1\2"]
    reg_string_md2 = [r"{ (.+) }", r"{\1}"]
    reg_string_list = []
    reg_string_list.append(reg_string_md)
    perform_regex_rename_on_files(reg_string_list, path, files_md)
    dirs = [directory for directory in os.listdir(
        path) if os.path.isdir(directory)]
    reg_string_list = []
    reg_string_list.append(reg_string_dir)
    perform_regex_rename_on_files(reg_string_list, path, dirs)


def perform_regex_rename_on_files(reg_string_list, path=None, files=None):
    if path is None:
        path = os.getcwd()
    if files is None:
        files = os.listdir(path)

    for file in files:
        for reg_string in reg_string_list:
            match = re.search(reg_string[0], file)
            if match is not None:
                new_file = re.sub(reg_string[0], reg_string[1], file)
                try:
                    os.rename(file, new_file)
                    print(f"Renamed '{file}' to '{new_file}'")
                except OSError as e:
                    print(f"Error renaming '{file}' to '{new_file}': {e}")


def md_note_process(num=0, head_num=1):
    import md_helper
    operations = {
        1: remove_back_matter_and_copy_code,
        2: md_helper.degrade_markdown_by_head_number,
        3: md_helper.retrieve_document_summary_info,
        4: md_helper.format_ocr_text,

    }

    if num in operations:
        if num == 2:
            operations[num](head_num)
        else:
            operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def remove_back_matter_and_copy_code(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_Back_matter_template = [r"---\n\n- created:.+\n- source: .+", r""]
    reg_string_list.extend([reg_Back_matter_template])
    reg_string_copy_code = [r"```\n(.+)Copy code", r"```\1\n"]
    reg_string_list.extend([reg_string_copy_code])
    perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def wiki_note_process(num=0):
    operations = {
        1: remove_wiki_edit_link,
        2: remove_wiki_equation_svg,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def remove_wiki_edit_link(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_wiki_edit_link = [
        r'\\\[\[edit\]\(https://en\.wikipedia\.org/w/index\.php\?title=.+ "Edit section: (.+)"\)\\\]', r""]
    reg_string_list.extend([reg_wiki_edit_link])

    perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def remove_wiki_equation_svg(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_wiki_equation_svg = [r'!\[([^\]]+)\]\([A-Za-z0-9]+\.svg\)', r"$\1$"]

    reg_string_list.extend([reg_wiki_equation_svg])

    perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def vid_note_process(num=0):
    import vid_note_processor
    operations = {
        1: vid_note_processor.initialize_vid_note_file_structure,
        2: vid_note_processor.generate_vid_note_with_timeline_from_text_summary,
        3: vid_note_processor.generate_vid_note_with_timeline_from_timestamps,
        4: vid_note_processor.convert_md_vid_link_to_html,
        5: vid_note_processor.convert_md_vid_link_to_html_tree,
        6: vid_note_processor.vtt_format_4_gpt,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def get_bvid_reg_string(sub_topic1_to_sub_topicn_folder_list, TR_MODE=0):

    # sub_topic=sub_topic1_to_sub_topicn_folder_list[-2].split("_")[-2]+" "+sub_topic1_to_sub_topicn_folder_list[-2].split("_")[-1]
    # sub_topic=sub_topic1_to_sub_topicn_folder_list[-2].split("_")[-1]
    reg_sub = [r'\d{3}_(.+)', r'\1']

    match = re.search(reg_sub[0], sub_topic1_to_sub_topicn_folder_list[-2])
    if match:
        sub_topic1 = re.sub(reg_sub[0], reg_sub[1],
                            sub_topic1_to_sub_topicn_folder_list[-2])
        sub_topic1.replace("_", " ")
    else:
        raise Exception("sub_topic1 not found")
    if TR_MODE:
        print("Sub topic1:", sub_topic1)
    current_topic = sub_topic1_to_sub_topicn_folder_list[-1].split("_")[-1]
    if TR_MODE:
        print("Current topic:", current_topic)
    bvid_reg_string = current_topic+r'(( - )|(- - ))'+sub_topic1+r'\.mp4'
    if TR_MODE:
        print("bvid_reg_string:", bvid_reg_string)
    bvid_srt_reg_string = current_topic + \
        r'(( - )|(- - ))'+sub_topic1+r'(\.en|\.en.+)'+r'\.srt'
    return bvid_reg_string, bvid_srt_reg_string


def os_file_processor(num=0):
    import file_operations_utils
    operations = {
        1: get_kg_bassets_folder_keyword,
        2: add_timestamp_to_filenames,
        3: get_current_timestamp,
        4: file_operations_utils.zfill_folder_files,
        5: file_operations_utils.rename_folders_4_mooc_b,
        6: file_operations_utils.initialize_notes_files_structure,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


# def get_prompt_explain_c_cpp():
#     import prompts
#     prompts.get_prompt_explain_c_cpp()


def get_prompts(num=0):
    import prompts
    operations = {
        1: prompts.video_summarization_expert_one,
        2: prompts.get_prompt_explain_c_cpp,
        3: prompts.chatbot_prompt_expert,
        4: prompts.Translate_Chinese_sentence_into_function_name,
        5: prompts.Expert_Prompt_Creator,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def main():
    # create a parser object
    parser = argparse.ArgumentParser()

    # add arguments for each function
    parser.add_argument('-t', '--timestamp', type=str, default=r'1676880280',
                        help='input timestamp to pass to the function')
    parser.add_argument('-u', '--str_url', type=str, default=r'test',
                        help='input str_url to pass to the function')
    parser.add_argument('-ii', '--input_int', type=int, default=r'0',
                        help='input input_int to pass to the function')
    parser.add_argument('-hn', '--head_num', type=int, default=r'1',
                        help='input head_num to pass to the function')
    parser.add_argument('-gt', '--get_timestamp',
                        action='store_true', help='call get_current_timestamp')
    parser.add_argument('-at', '--add_timestamp', action='store_true',
                        help='call add_timestamp_to_filenames')

    parser.add_argument('-mdx', '--mdx2md',
                        action='store_true', help='call mdx2md')
    parser.add_argument('-oaf', '--open_b_assets_folder',
                        action='store_true', help='call open_b_assets_folder')

    parser.add_argument('-md', '--md_note_process',
                        action='store_true', help='call md_note_process')
    parser.add_argument('-wiki', '--wiki_note_process',
                        action='store_true', help='call wiki_note_process')
    parser.add_argument('-vid', '--vid_note_process',
                        action='store_true', help='call vid_note_process')
    parser.add_argument('-tt', '--timestamps_3blue1brown_2_timeline',
                        action='store_true', help='call timestamps_3blue1brown_2_timeline')
    parser.add_argument('-cti', '--copy_timestamps_and_index_2_root',
                        action='store_true', help='call copy_timestamps_and_index_2_root')
    parser.add_argument('-csm', '--convert_subtitle_chatgpt_summary_to_markdown_vid_timeline',
                        action='store_true', help='call convert_subtitle_chatgpt_summary_to_markdown_vid_timeline')
    parser.add_argument('-cssm', '--convert_subtitle_and_summary_to_markdown_vid_timeline',
                        action='store_true', help='call convert_subtitle_and_summary_to_markdown_vid_timeline')

    parser.add_argument('-ci', '--create_imgs_folder',
                        action='store_true', help='call create_directory_assets_imgs')
    parser.add_argument('-cc', '--creat_concept_folder', action='store_true',
                        help='call create_directory_assets_concept_structure')
    parser.add_argument('-css', '--creat_subtitle_summary', action='store_true',
                        help='call create_file_subtitle_summary_gpt_md')
    parser.add_argument('-h2m', '--html2md',
                        action='store_true', help='call html2md')
    parser.add_argument('-h2m2', '--html2md2',
                        action='store_true', help='call html2md2')

    parser.add_argument('-h2mt', '--html2md_tree',
                        action='store_true', help='call html2md_tree')
    parser.add_argument('-m2hl', '--convert_md_vid_link_to_html',
                        action='store_true', help='call convert_md_vid_link_to_html')
    parser.add_argument('-init', '--initialize_vid_note_file_structure',
                        action='store_true', help='call initialize_vid_note_file_structure')
    parser.add_argument('-test', '--test',
                        action='store_true', help='call test')
    parser.add_argument('-zbp', '--zhi_book_process',
                        action='store_true', help='call zhi_book_process')
    parser.add_argument('-osf', '--os_file_processor',
                        action='store_true', help='call os_file_processor')
    parser.add_argument('-vls', '--full_fill_vid_link_2_summary',
                        action='store_true', help='call full_fill_vid_link_2_summary')
    parser.add_argument('-gp', '--get_prompts',
                        action='store_true', help='call get_prompts')
    # parse the command-line arguments
    args = parser.parse_args()

    # call the appropriate function based on the arguments
    if args.md_note_process:
        md_note_process(args.input_int, args.head_num)
    elif args.wiki_note_process:
        wiki_note_process(args.input_int)
    elif args.vid_note_process:
        vid_note_process(args.input_int)
    elif args.copy_timestamps_and_index_2_root:
        copy_timestamps_and_index_2_root()
    elif args.convert_subtitle_chatgpt_summary_to_markdown_vid_timeline:
        convert_subtitle_chatgpt_summary_to_markdown_vid_timeline(args.str_url)
    elif args.convert_subtitle_and_summary_to_markdown_vid_timeline:
        convert_subtitle_and_summary_to_markdown_vid_timeline(args.str_url)
    elif args.mdx2md:
        mdx2md(args.timestamp)
    elif args.open_b_assets_folder:
        open_b_assets_folder()
    elif args.timestamps_3blue1brown_2_timeline:
        timestamps_3blue1brown_2_timeline(args.str_url)
    elif args.get_timestamp:
        get_current_timestamp()
    elif args.add_timestamp:
        add_timestamp_to_filenames()

    elif args.create_imgs_folder:
        create_directory_assets_imgs()
    elif args.creat_concept_folder:
        create_directory_assets_concept_structure()
    elif args.creat_subtitle_summary:
        create_file_subtitle_summary_gpt_md()
    elif args.html2md:
        html2md()
    elif args.html2md2:
        html2md2()
    elif args.html2md_tree:
        html2md_tree()
    elif args.convert_md_vid_link_to_html:
        convert_md_vid_link_to_html()
    elif args.initialize_vid_note_file_structure:
        initialize_vid_note_file_structure()

    elif args.test:
        test(args.input_int)

    elif args.zhi_book_process:
        zhi_book_process(args.input_int)
    elif args.os_file_processor:
        os_file_processor(args.input_int)
    elif args.get_prompts:
        get_prompts(args.input_int)
    else:
        print("Invalid argument")


if __name__ == "__main__":
    main()
