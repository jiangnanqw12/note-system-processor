import urllib.parse
import chardet
import os
import re
import time
import pyperclip
import glob
import subprocess

# 需求1 rename files


def get_father_path(path):
    return os.path.dirname(path)


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


def find_files_with_multiple_extensions(base_path, extensions):
    """
    Find files in the given base_path with the specified extensions.

    Args:
        base_path (str): The directory in which to search for files.
        extensions (list of str): A list of file extensions to include in the search.

    Returns:
        list of str: A list of file paths that match the given extensions.
    """
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(base_path, f"*.{ext}")))
    return files


def test_find_files_with_multiple_extensions():
    # Example usage
    base_path = '/path/to/your/directory'
    extensions = ['c', 'cpp', 'hpp', 'h']
    all_files = find_files_with_multiple_extensions(base_path, extensions)


def rename_order0(base_path):
    """
    .*_{timestamp before}.svg
    ->
    .*_{timestamp}.svg
    """
    # files_svg = [f for f in os.listdir(base_path) if f.endswith(".svg")]
    files_svg = glob.glob(os.path.join(base_path, "*.svg"))
    pattern_timestamp_svg = re.compile(r"(.*)_(\d{10})\.svg")

    timestamp = get_current_timestamp()
    for file in files_svg:
        match = pattern_timestamp_svg.match(file)
        if match:
            print("timestamp before: ", match.group(2))
            new_name = f"{match.group(1)}_{timestamp}.svg"
            os.rename(file, os.path.join(base_path, new_name))


def rename_order1(base_path):
    import pattern_replacement
    for root, dirs, files in os.walk(base_path):
        for file in files:
            match = re.search(
                pattern_replacement.pattern_subtile_summary_gpt_timestamps_files, file)
            if match:
                print(f"Old file name: {file}")
                new_file_name = f"{match.group(1)}_{match.group(2)}.txt"
                print(f"New file name: {new_file_name}")
                # Rename the file
                old_file_path = os.path.join(root, file)
                new_file_path = os.path.join(root, new_file_name)
                os.rename(old_file_path, new_file_path)


def rename_order2(base_path):
    """
        cs50 note
        999_index
        Week (\d{1,3}) (.+)
        +
        Lecture (\d{1,3}) - CS50x 2023\.md
        -->
        f"{lecture_number+1:03d}_{lecture[lecture_number]}.md"
        """

    import flags_utils
    flags = flags_utils.get_flag_default()
    TR_MODE = flags.get_flag("TR_MODE")

    with open(os.path.join(base_path, "999_index.md"), "r") as f:
        index_list = f.read().splitlines()
    lecture = dict()
    for index in index_list:
        reg = r"Week (\d{1,3}) (.+)"
        match = re.match(reg, index)
        if match:
            week_number = int(match.group(1))

            week_name = match.group(2).strip()
            lecture[week_number] = week_name
            if TR_MODE:
                print(f"Week {week_number} - {week_name}")
    # files_md = [f for f in os.listdir(base_path) if f.endswith(".md")]
    files_md = glob.glob(os.path.join(base_path, "*.md"))
    for file in files_md:
        reg = r"Lecture (\d{1,3}) - CS50x 2023\.md"
        match = re.match(reg, file)
        if match:
            lecture_number = int(match.group(1))
            if TR_MODE:
                print(f"Lecture {lecture_number}")
            new_file_name = f"{lecture_number+1:03d}_{lecture[lecture_number]}.md"
            if TR_MODE:
                print(f"Renaming {file} to {new_file_name}")
            os.rename(os.path.join(base_path, file),
                      os.path.join(base_path, new_file_name))


def rename_order3(base_path):
    """
    /index/*.mp4
        to
        /index_*.mp4
    """
    # files_mp4 = [f for f in os.listdir(base_path) if f.endswith(".mp4")]
    files_mp4 = glob.glob(os.path.join(base_path, "*.mp4"))
    for index in range(16):
        start_str = f"{16 - index:03d}_"
        for file_mp4 in files_mp4:
            if file_mp4.startswith(start_str):
                new_file = f"{1+index:03d}{file_mp4[3:]}"
                os.rename(os.path.join(base_path, file_mp4),
                          os.path.join(base_path, new_file))


def rename_order4(base_path):
    """
/index/*.mp4
to
/16-index_*.mp4
"""
    for index in range(16):
        dir_path = os.path.join(base_path, f"{16 - index}")

        # Check if the directory exists
        if not os.path.isdir(dir_path):
            print(f"Directory '{dir_path}' does not exist. Skipping.")
            continue

        try:
            for file in os.listdir(dir_path):
                old_file_path = os.path.join(dir_path, file)
                # Zero-padded prefix
                new_file_name = f"{16 - index:03d}_{file}"
                new_file_path = os.path.join(base_path, new_file_name)
                os.rename(old_file_path, new_file_path)
                print(f"Renamed '{old_file_path}' to '{new_file_path}'")
        except OSError as e:
            print(f"Error renaming files in '{dir_path}': {e}")


def rename_order5(base_path):
    """
    (\d{1,4}\.)(.+)
    -->
    \1 \2
    """
    folders = [f for f in os.listdir(
        base_path) if os.path.isdir(os.path.join(base_path, f))]
    for folder in folders:
        match = re.search(r"(\d{1,4}\.)(.+)", folder)
        if match:
            new_folder = f"{match.group(1)} {match.group(2)}"
            os.rename(os.path.join(base_path, folder),
                      os.path.join(base_path, new_folder))


def rename_order6(base_path):
    """
    (\d{1,4}\.)(.+)(\.md|\.svg)
    -->
    \1 \2\3
    """
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith(".md") or file.endswith(".svg"):
                match = re.search(r"(\d{1,4}\.)(.+)(\.md|\.svg)", file)
                if match:
                    new_file = f"{match.group(1)} {match.group(2)}{match.group(3)}"
                    os.rename(os.path.join(root, file),
                              os.path.join(root, new_file))


def rename_files_in_directories_orders(base_path=None, order=5):
    import flags_utils
    flags = flags_utils.get_flags_default()
    TR_MODE = flags.get_flag("TR_MODE")
    """

    Rename all files in numbered directories within the base path.
    Each file is prefixed with the directory number, zero-padded to three digits.
    """
    # Use the current working directory if no path is provided
    base_path = base_path or os.getcwd()

    # Validate the base path
    if not os.path.isdir(base_path):
        print(f"The provided path '{base_path}' is not a valid directory.")
        return
    try:
        if order == 0:
            rename_order0(base_path)
        elif order == 1:
            rename_order1(base_path)

        elif order == 2:
            rename_order2(base_path)
        elif order == 3:
            rename_order3(base_path)
        elif order == 4:
            rename_order4(base_path)
        elif order == 5:
            rename_order5(base_path)
        elif order == 6:
            rename_order6(base_path)
        elif order == 7:
            pass
        elif order == 8:
            pass
        elif order == 9:
            pass
        elif order == 10:
            pass
        elif order == 11:
            pass
        else:
            raise ValueError(f"Unrecognized order: {order}")
        if TR_MODE:
            print(
                f"Files successfully renamed in {base_path} using order {order}.")
    except Exception as e:
        raise ValueError(f"An error occurred during renaming: {e}")


def rename_files_in_directories(base_path=None):
    rename_files_in_directories_orders(order=6, base_path=base_path)


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


def get_Topic_in_kg(TR_MODE=0):
    assets_sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = get_kg_assets_root()
    if TR_MODE:
        print("assets_sub_topic1_to_sub_topicn_folder_list:",
              assets_sub_topic1_to_sub_topicn_folder_list)
        print("OneDrive KG root directory_path:",
              OneDrive_KG_note_root_directory_path)
    Topic = os.path.basename(OneDrive_KG_note_root_directory_path)
    if TR_MODE:
        print("Topic:", Topic)
    num_topic = len(assets_sub_topic1_to_sub_topicn_folder_list)
    reg_sub1 = [r'\d{3}_(.+)', r'\1']
    if num_topic < 1:
        sub_topic1 = None
    elif num_topic >= 1:
        sub_topic1 = assets_sub_topic1_to_sub_topicn_folder_list[0]
        match = re.search(reg_sub1[0], sub_topic1)
        if match:
            sub_topic1 = re.sub(reg_sub1[0], reg_sub1[1], sub_topic1)
            if TR_MODE:
                print("sub_topic1:", sub_topic1)

    return Topic, sub_topic1


def perform_regex_replacement_on_files(reg_string_list, path=None, files=None):

    if path is None:
        path = os.getcwd()
    if files is None:
        files = os.listdir(path)

    for file in files:

        with open(os.path.join(path, file), "r", encoding="utf-8") as f1:
            content = f1.read()
        for regex in reg_string_list:
            content = re.sub(regex[0], regex[1], content)
        with open(os.path.join(path, file), "w", encoding="utf-8") as f:
            f.write(content)


def perform_regex_replacement_on_files_tree(reg_string_list, path=None):

    if path is None:
        path = os.getcwd()

    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)

            with open(file_path, "r", encoding="utf-8") as f1:
                content = f1.read()

            new_content = content
            for regex in reg_string_list:
                new_content = re.sub(regex[0], regex[1], new_content)

            if new_content != content:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)


def get_bvids_origin_topic_path(Topic, TR_MODE=0):
    # bvids_origin_topic_path = get_bvids_origin_topic_path(BaiduSyncdisk_assets_root)
    # bvids_origin_topic_path = r"C:\BaiduSyncdisk\Multivariable_calculus_Khan_Academy_youtube"
    # bvids_origin_topic_path=r'C:\BaiduSyncdisk\First Principles of Computer Vision Specialization\Features and Boundaries'
    bvids_origin_topic_path = r'C:\BaiduSyncdisk\00_MOOC_b'
    # bvids_origin_topic_path=r'C:\BaiduSyncdisk\deep'
    # bvids_origin_topic_path=r'C:\BaiduSyncdisk\Introduction'

    if Topic is None:
        raise Exception("Topic is None")
    bvids_origin_topic_path = os.path.join(
        bvids_origin_topic_path, Topic)
    if TR_MODE:
        print("bvids_origin_topic_path:", bvids_origin_topic_path)
    # if os.path.basename(bvids_origin_topic_path) != Topic:
    #     print("bvids_origin_topic_path:", bvids_origin_topic_path)
    #     print("Topic:", Topic)

    #     raise Exception("Topic name not match")
    return bvids_origin_topic_path


def get_kg_assets_root(current_dir=None):
    '''

    '''
    TR_MODE = 1
    if current_dir is None:
        current_dir = os.getcwd()
    sub_topic1_to_sub_topicn_folder_list = []

    while True:

        if 'assets' in os.listdir(current_dir):
            sub_topic1_to_sub_topicn_folder_list.reverse()

            return sub_topic1_to_sub_topicn_folder_list, current_dir

        else:
            sub_topic1_to_sub_topicn_folder_list.append(
                os.path.basename(current_dir))
            current_dir = os.path.dirname(current_dir)


def create_file_subtitle_summary_gpt_md(path=None):
    # Create a file named subtitle.md and summary_gpt.md
    print("create_file_subtitle_summary_gpt_md")
    if path is None:
        path = os.getcwd()
    time_stamp = int(time.time())
    with open(os.path.join(path, "subtitle_"+str(time_stamp)+".md"), "w") as f:
        pass
    with open(os.path.join(path, "summary_gpt_"+str(time_stamp)+".md"), "w") as f:
        pass
    with open(os.path.join(path, "timestamps_"+str(time_stamp)+".md"), "w") as f:
        pass


def get_note_assets_dir_path(sub_topic1_to_sub_topicn_folder_list, current_dir):
    # sub_topic1_to_sub_topicn_folder_list.append(os.path.basename(current_dir))
    # current_dir = os.path.dirname(current_dir)
    while True:

        if 'assets' in os.listdir(current_dir):
            sub_topic1_to_sub_topicn_folder_list.reverse()
            if sub_topic1_to_sub_topicn_folder_list != []:
                note_assets_dir_path = os.path.join(current_dir, 'assets')
                for folder_name in sub_topic1_to_sub_topicn_folder_list:
                    note_assets_dir_path = os.path.join(
                        note_assets_dir_path, folder_name)
                    # print(note_assets_dir_path)
                    # if os.path.isdir(note_assets_dir_path):
                    if not os.path.exists(note_assets_dir_path):
                        os.makedirs(note_assets_dir_path)
                return note_assets_dir_path
                # else:
                #     raise Exception('not a directory ',note_assets_dir_path)
            else:
                raise Exception("No folder name found")

            break
        else:
            sub_topic1_to_sub_topicn_folder_list.append(
                os.path.basename(current_dir))
            current_dir = os.path.dirname(current_dir)


def initialize_notes_files_structure():
    TR_mode = 1
    import urllib.parse

    # Get the current directory
    current_directory = os.getcwd()
    if TR_mode:
        print(f"Current directory: {current_directory}")

    # Get the parent directory
    parent_directory = os.path.dirname(current_directory)
    if TR_mode:
        print(f"Parent directory: {parent_directory}")

        # Get the name of the current directory
    current_directory_name = os.path.basename(current_directory)
    if TR_mode:
        print(f"Current directory name: {current_directory_name}")

    # Get the name of the parent directory
    parent_directory_name = os.path.basename(parent_directory)
    if TR_mode:
        print(f"Parent directory name: {parent_directory_name}")
    timestamp = int(time.time())
    start_file = f"000_{parent_directory_name}_{current_directory_name}_{timestamp}.md"
    url_start_file = urllib.parse.quote(start_file)
    url_start_file = rf"{current_directory_name} [📄]({url_start_file})"
    # start_file = "000_"+current_directory_name+"_"+parent_directory_name+".md"
    if TR_mode:
        print(f"start_file: {start_file}\n{url_start_file}")
    # Check if file exists, if not create it
    start_file__directory = os.path.join(current_directory, start_file)
    if not os.path.exists(start_file__directory):
        with open(start_file__directory, 'w') as f:
            # creating an empty markdown file
            f.write(f'\n{current_directory_name}\n')
    string_list = current_directory_name.split("_")
    len_string_list = len(string_list)
    if len_string_list < 1:
        raise ValueError("len error")
    elif len_string_list == 1:
        if len(string_list[0]) < 2:
            raise ValueError("len error")
        folder_b_assets = string_list[0][0] + \
            string_list[-1][-1]+"_"+str(timestamp)
    elif len_string_list > 1:
        folder_b_assets = string_list[0][0] + \
            string_list[-1][0]+"_"+str(timestamp)
    if TR_mode:
        print("folder_b_assets: ", folder_b_assets)
    assets_directory = os.path.join(current_directory, "assets")
    # Check if 'assets' directory exists, if not create it
    if not os.path.exists(assets_directory):
        os.mkdir(assets_directory)
        if TR_mode:
            print(f"'assets' directory created in {current_directory}")
    b_assets_directory = os.path.join(assets_directory, folder_b_assets)
    if not os.path.exists(b_assets_directory):
        os.mkdir(b_assets_directory)
        if TR_mode:
            print(
                f"b_assets_directory directory created in {b_assets_directory}")
    file_git_ignore = os.path.join(b_assets_directory, ".gitignore")
    if not os.path.exists(file_git_ignore):
        with open(file_git_ignore, 'w') as f:

            f.write('*.flv\n*.mp4\n*.srt\n*.vtt\n*.pdf\n*.epub\n*.pptx\n')
    file_readme = os.path.join(b_assets_directory, "readme.md")
    if not os.path.exists(file_readme):
        with open(file_readme, 'w') as f:
            f.write(current_directory_name+"\n")


def rename_folders_4_mooc_b(path=None, zfill_num=3):
    if path is None:
        path = os.getcwd()
    import flags_utils

    Flags = flags_utils.GlobalFlags()
    Flags.set_flag('TR_MODE', 1)
    TR_MODE = Flags.get_flag('TR_MODE')
    # files_mp4 = [f for f in os.listdir(
    #     path) if f.endswith(".mp4")]
    # files_vtt = [f for f in os.listdir(
    #     path) if f.endswith(".vtt")]
    # files_srt = [f for f in os.listdir(
    #     path) if f.endswith(".srt")]
    files = os.listdir(path)
    # for file_mp4 in files_mp4:

    # r"How Ultrasonic Energy is Created _ Science of Energy Ep. 1 _ Ethicon-Bd2xISKVyFc.mp4"
    r"Monopolar Electrosurgery Technology and Principles - Science of Energy Ep. 5 - E.en.srt"
    reg_string_vid1 = [
        r'(.+) ｜ Fuzzy Logic.+Part (\d{1,2})\.mp4', '']
    reg_string_sub1 = [
        r"(.+) ｜ Fuzzy Logic.+Part (\d{1,2})(\.en|\.eng|\.zh|\.cn|\.zho|\.chi|\.zh-Hans|\.zh-Hant|)-eEY6OEpapPo(\.vtt|\.srt)", r'\1']
    reg_string_vid2 = [
        r'(.+) - Science of Energy Ep. (\d{1,2}) -.+\.mp4', '']
    reg_string_sub2 = [
        r"(.+) - Science of Energy Ep. (\d{1,2}) -.+\.en\.srt", r'\1']
    reg_sring_vid = reg_string_vid1
    reg_sring_sub = reg_string_sub1
    for file in files:
        match = re.search(reg_sring_vid[0], file)
        if match:

            series_num = match.group(2)
            series_num = series_num.zfill(zfill_num)
            reg_string_vid_replace = series_num+"_"+r"\1"+".mp4"
            if TR_MODE:
                print("reg_string_vid_replace is:", reg_string_vid_replace)
            file_name = re.sub(reg_sring_vid[0], reg_string_vid_replace, file)
            if TR_MODE:
                print(file_name)

            os.rename(os.path.join(path, file), os.path.join(
                path, file_name))
        match = re.search(reg_sring_sub[0], file)
        if match:

            series_num = match.group(2)
            series_num = series_num.zfill(zfill_num)
            reg_string_sub_replace = series_num+"_"+r"\1"+r"\3"+r"\4"
            if TR_MODE:

                print("reg_string_sub_replace is:\n", reg_string_sub_replace)
            file_name = re.sub(reg_sring_sub[0], reg_string_sub_replace, file)
            if TR_MODE:
                print("file_name is :\n", file_name)

            os.rename(os.path.join(path, file), os.path.join(
                path, file_name))


def zfill_folder_files(path=None, zfill_num=3):
    if path is None:
        path = os.getcwd()

    files = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    for file in files:
        file_name, file_ext = os.path.splitext(file)
        file_name_zfilled = file_name.zfill(zfill_num)
        os.rename(os.path.join(path, file), os.path.join(
            path, file_name_zfilled + file_ext))
    dirs = [f for f in os.listdir(
        path) if os.path.isdir(os.path.join(path, f))]
    for dir in dirs:
        dir_name, dir_ext = os.path.splitext(dir)
        dir_name_zfilled = dir_name.zfill(zfill_num)
        os.rename(os.path.join(path, dir), os.path.join(
            path, dir_name_zfilled + dir_ext))


def get_kg_bassets_folder_keyword():
    TR_MODE = 1
    sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = get_kg_assets_root()

    if TR_MODE:
        print("Folder list:", sub_topic1_to_sub_topicn_folder_list)
        print("OneDrive KG root directory_path:",
              OneDrive_KG_note_root_directory_path)
    OneDrive_KG_assets_directory_path = os.path.join(
        OneDrive_KG_note_root_directory_path, "assets")
    if TR_MODE:
        print("OneDrive KG assets directory_path:",
              OneDrive_KG_assets_directory_path)
    dirs = [directory for directory in os.listdir(OneDrive_KG_assets_directory_path) if os.path.isdir(
        os.path.join(OneDrive_KG_assets_directory_path, directory))]
    if TR_MODE:
        print("dirs:", dirs)
    reg_string = [r".+_\d{10}", r"\1"]
    for dir in dirs:
        match = re.search(reg_string[0], dir)
        if match:
            if TR_MODE:
                print("match.group(0):", match.group(0))
            keyword_path = os.path.join(OneDrive_KG_assets_directory_path, dir)
            if TR_MODE:
                print("keyword_path:", keyword_path)
            return match.group(0), keyword_path


def get_bassets_keyword_path(current_dir=None, key_word="mc_1683793602"):
    '''
    kg and bkg 中的 bassets path
    '''
    TR_MODE = 1
    if current_dir is None:
        current_dir = os.getcwd()
    keyword_sub_topic1_to_sub_topicn_folder_list = []

    keyword_sub_topic1_to_sub_topicn_folder_list.append(
        os.path.basename(current_dir))
    current_dir = os.path.dirname(current_dir)
    while True:

        if 'assets' in os.listdir(current_dir):
            keyword_sub_topic1_to_sub_topicn_folder_list.reverse()

            keyword_sub_topic1_to_sub_topicn_folder_list.insert(1, key_word)
            return keyword_sub_topic1_to_sub_topicn_folder_list, current_dir

        else:
            keyword_sub_topic1_to_sub_topicn_folder_list.append(
                os.path.basename(current_dir))
            current_dir = os.path.dirname(current_dir)


def get_Topic_in_kg_assets(TR_MODE=0):
    assets_sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = get_kg_assets_root()
    if TR_MODE:
        print("assets_sub_topic1_to_sub_topicn_folder_list:",
              assets_sub_topic1_to_sub_topicn_folder_list)
        print("OneDrive KG root directory_path:",
              OneDrive_KG_note_root_directory_path)
    Topic = os.path.basename(OneDrive_KG_note_root_directory_path)
    if TR_MODE:
        print("Topic:", Topic)
    num_topic = len(assets_sub_topic1_to_sub_topicn_folder_list)
    reg_sub1 = [r'\d{3}_(.+)', r'\1']
    if num_topic <= 1:
        raise Exception("num_topic<=1")
    elif num_topic == 2:
        sub_topic1 = None

    elif num_topic >= 3:

        match = re.search(
            reg_sub1[0], assets_sub_topic1_to_sub_topicn_folder_list[1])
        if match:
            sub_topic1 = re.sub(reg_sub1[0], reg_sub1[1],
                                assets_sub_topic1_to_sub_topicn_folder_list[1])
            if TR_MODE:
                print("sub_topic1:", sub_topic1)
        else:
            raise Exception("sub_topic1 not found")

    current_topic = assets_sub_topic1_to_sub_topicn_folder_list[-1]
    current_topic = re.sub(reg_sub1[0], reg_sub1[1], current_topic)
    return Topic, sub_topic1, current_topic


def get_b_KG_directory_path(path=None):
    if path is None:
        path = os.getcwd()

    if path.find("OneDrive") == -1 or path.find("KG") == -1:
        raise Exception("This script is only for use with OneDrive/KG.")
    # if path.find("assets") ==-1:
    #     raise Exception("current path is not an assets path.")
    # reg_search=[r'(.+\\OneDrive\\KG\\)(.+)']
    reg_search = [
        [r'.+\\OneDrive\\KG\\(.+)', r'C:\\BaiduSyncdisk\\assets\\\1']]
    test2 = r'C:\BaiduSyncdisk\assets\O\O1\O17\O172\Multivaribale_calculus_Khan_Academy\assets\bvids\mc_1683793602\001_\005_'
    test = r'C:\Users\shade\OneDrive\KG\O\O1\O17\O172\Multivaribale_calculus_Khan_Academy\assets\001_Thinking about multivariable functions\005_Transformations\003_Transformations, part 3'
    # print(path)
    match1 = re.search(reg_search[0][0], path)
    if match1:
        path_b_assets = re.sub(reg_search[0][0], reg_search[0][1], path)
        # print(path_b_assets)
        return path_b_assets


def get_OneDrive_KG_note_path(OneDrive_KG_root, sub_topic1_to_sub_topicn_folder_list):
    OneDrive_KG_note_path = OneDrive_KG_root
    for i in range(2, len(sub_topic1_to_sub_topicn_folder_list)-1):
        OneDrive_KG_note_path = os.path.join(
            OneDrive_KG_note_path, sub_topic1_to_sub_topicn_folder_list[i])
    print(OneDrive_KG_note_path)
    return OneDrive_KG_note_path


def get_current_bvid_name(path=None):
    if path is None:
        path = os.getcwd()
    file = os.path.basename(path)
    return file+".mp4"


def get_bvids_destination_long(sub_topic1_to_sub_topicn_folder_list, BaiduSyncdisk_assets_root):
    path_temp = BaiduSyncdisk_assets_root
    for i in range(len(sub_topic1_to_sub_topicn_folder_list)-1):
        path_temp = os.path.join(
            path_temp, sub_topic1_to_sub_topicn_folder_list[i])

        if not os.path.exists(path_temp):
            os.makedirs(path_temp)
    return path_temp


def get_assets_root_path(current_dir=None):
    if current_dir is None:
        current_dir = os.getcwd()
    while True:
        if 'assets' in os.listdir(current_dir):
            return current_dir, os.path.basename(current_dir)
        else:
            current_dir = os.path.dirname(current_dir)
            if current_dir == '':
                raise Exception('assets folder not found')


def create_output_directory(root=None):
    if root is None:
        root = os.getcwd()

    output_dir = os.path.join(root, 'output')

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    # print("Created output directory %s" % output_dir)
    return output_dir


def create_new_file_name(file):
    if not file.endswith('.md'):
        filename_without_ext = os.path.splitext(file)[0]
        new_file_name = filename_without_ext+'.md'
    else:
        new_file_name = file
    print(new_file_name)
    return new_file_name


def create_excalidraw_file_based_on_content(content=None, path=None):
    write_string = """
---

excalidraw-plugin: parsed
tags: [excalidraw]

---
==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠==


%%
# Drawing
```json
{"type":"excalidraw","version":2,"source":"https://github.com/zsviczian/obsidian-excalidraw-plugin/releases/tag/1.9.19","elements":[],"appState":{"gridSize":null,"viewBackgroundColor":"#ffffff"}}
```
%%
"""
    ext = ".excalidraw" + ".md"
    create_file_based_on_content(
        write_string, ext, content, path)


def create_drawio_file_based_on_content(file_name_content=None, path=None):

    #     write_string = """
    # <svg xmlns="http://www.w3.org/2000/svg" version="1.1" height="0px" width="0px" viewBox="-10 -10 20 20" content="&lt;mxGraphModel dx=&quot;801&quot; dy=&quot;859&quot; grid=&quot;1&quot; gridSize=&quot;10&quot; guides=&quot;1&quot; tooltips=&quot;1&quot; connect=&quot;1&quot; arrows=&quot;1&quot; fold=&quot;1&quot; page=&quot;1&quot; pageScale=&quot;1&quot; pageWidth=&quot;827&quot; pageHeight=&quot;1169&quot; math=&quot;0&quot; shadow=&quot;0&quot;&gt;&lt;root&gt;&lt;mxCell id=&quot;0&quot;/&gt;&lt;mxCell id=&quot;1&quot; parent=&quot;0&quot;/&gt;&lt;/root&gt;&lt;/mxGraphModel&gt;"><style type="text/css"></style></svg>
    # """
    ext = ".drawio.svg"
    if path is None:
        path = os.getcwd()
    # get current script file path
    script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(script_path)
    svg_file = os.path.join(script_dir, "..", "assets",
                            "1707460474.drawio.svg")
    with open(svg_file, "r", encoding="utf-8") as file:
        write_string = file.read()

    draio_file_name = create_file_based_on_content(
        write_string, ext, file_name_content, path)
    return draio_file_name


def create_file_based_on_content(write_string="", ext="", content=None, path=None):
    if content is None:
        content = pyperclip.paste()
    if path is None:
        path = os.getcwd()

    if len(content) > 100:
        raise ValueError("Content length exceeds 100 characters")
    if len(content) < 1:
        raise ValueError("Content length is less than 1 character")

    if content.count("\n") > 2:
        raise TypeError("Content contains more than 2 newline characters")
    content = content.replace('\n', ' ')
    content = content.replace('\r', ' ')
    reg = [r"\s{2,}", r' ']
    content = re.sub(reg[0], reg[1], content)
    timestamp = str(int(time.time()))
    new_name = content.strip() + "_" + timestamp+ext

    with open(os.path.join(path, new_name), "w", encoding="utf-8") as file:

        file.write(write_string)
    return new_name

def rename_index_folder_files(base_dir=None):
    if base_dir is None:
        base_dir = os.getcwd()
    # Ensure the path is absolute
    base_dir = os.path.abspath(base_dir)

    # Iterate through the subdirectories under the base directory
    for subdir in os.listdir(base_dir):
        subdir_path = os.path.join(base_dir, subdir)
        if os.path.isdir(subdir_path):
            # Ensure the subdirectory name is numeric before proceeding
            if subdir.isnumeric():
                # Format the subdirectory name with leading zeros
                formatted_subdir = f"{int(subdir):04d}"

                # Use glob to find all .mp4 files in the subdirectory
                mp4_files = glob.glob(os.path.join(subdir_path, "*.mp4"))

                # Rename each .mp4 file
                for mp4_file in mp4_files:
                    basename = os.path.basename(mp4_file)
                    new_name = f"{formatted_subdir}_{basename}"
                    new_path = os.path.join(base_dir, new_name)
                    os.rename(mp4_file, new_path)


def rename_bilibili_subs(path=None):
    ''' 重命名下载的字幕，改成视频名'''
    if path is None:
        path = os.getcwd()
    files_mp4 = glob.glob(os.path.join(path, "*.mp4"))
    files_srt = glob.glob(os.path.join(path, "*.srt"))
    for file_mp4 in files_mp4:
        basename = os.path.basename(file_mp4)

        new_name = f"{basename.split('.')[0]}.srt"
        new_path = os.path.join(path, new_name)
        for file_srt in files_srt:
            mp4 = (basename.split('.')[0]).split('_')[1]
            if mp4 in file_srt:
                os.rename(file_srt, new_path)


def convert_to_utf8(directory=None):

    if directory == None:
        directory = os.getcwd()

    files = os.listdir(directory)
    for file in files:
        if file.endswith('.c') or file.endswith('.cpp') or file.endswith('.h') or file.endswith('.hpp'):
            filepath = os.path.join(directory, file)
            if os.path.isfile(filepath):
                # Detect file encoding
                with open(filepath, 'rb') as file:
                    raw_data = file.read()
                    result = chardet.detect(raw_data)
                    file_encoding = result['encoding']

                if file_encoding != 'utf-8':
                    # Read file content
                    with open(filepath, 'r', encoding=file_encoding) as file:
                        content = file.read()

                    # Convert content to UTF-8 and save
                    with open(filepath, 'w', encoding='utf-8') as file:
                        file.write(content)


def print_tree(directory=None, prefix=''):
    if directory is None:
        directory = os.getcwd()
    files = os.listdir(directory)
    print(prefix + os.path.basename(directory) + '/')
    prefix = prefix + "|    "

    for i, file in enumerate(files):
        path = os.path.join(directory, file)
        if os.path.isdir(path):
            print_tree(path, prefix)
        else:
            print(prefix + file)


def generate_mermaid_structure(path, parent_node=None, mermaid_code=None, level=0):
    if mermaid_code is None:
        mermaid_code = ["graph TD;"]

    for item in os.listdir(path):
        full_path = os.path.join(path, item)
        node_name = f"{level}_{item}".replace(' ', '_').replace('.', '_')
        if parent_node:
            mermaid_code.append(f"    {parent_node} --> {node_name}")

        if os.path.isdir(full_path):
            generate_mermaid_structure(
                full_path, node_name, mermaid_code, level + 1)
        else:
            mermaid_code.append(f"    class {node_name} File;")

    return mermaid_code


def leet_code_files_init(base_path=None):

    if base_path is None:
        base_path = os.getcwd()
    # get current directory name
    current_dir_name = os.path.basename(base_path)
    drawio_file = create_drawio_file_based_on_content(
        file_name_content=current_dir_name, path=base_path)
    url_encoded_drawio_file_name = urllib.parse.quote(drawio_file)
    md_file_name = current_dir_name + ".md"
    # create a new markdown file if it does not exist
    if not os.path.exists(os.path.join(base_path, md_file_name)):
        with open(os.path.join(base_path, md_file_name), "w") as f:
            f.write(f"## Question\n\n")
            f.write(f"## Solution\n\n")
            f.write(f"![]({url_encoded_drawio_file_name})\n")
    master_solution_cpp_file_name = "master_solution1.cpp"
    # create a new cpp file if it does not exist
    if not os.path.exists(os.path.join(base_path, master_solution_cpp_file_name)):
        with open(os.path.join(base_path, master_solution_cpp_file_name), "w") as f:
            f.write(f"")
    student_solution_cpp_file_name = "student_solution1.cpp"
    # create a new cpp file if it does not exist
    if not os.path.exists(os.path.join(base_path, student_solution_cpp_file_name)):
        with open(os.path.join(base_path, student_solution_cpp_file_name), "w") as f:
            f.write(f"")



def remove_all_out_exe_files(path=None):
    if path is None:
        path = os.getcwd()
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".exe") or file.endswith(".out"):
                os.remove(os.path.join(root, file))

def main():
    print_tree()


if __name__ == "__main__":
    main()
