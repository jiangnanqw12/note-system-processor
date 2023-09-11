import os
import re
import time
import urllib.parse
import aspose.words as aw

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
