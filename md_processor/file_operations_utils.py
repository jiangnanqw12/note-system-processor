import os
import re
import time


def initialize_notes_files_structure():
    TR_mode = 1
    timestamp = int(time.time())
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

    start_file = "000_"+current_directory_name+"_"+parent_directory_name+".md"
    if TR_mode:
        print(f"start_file: {start_file}")
    # Check if file exists, if not create it
    start_file__directory = os.path.join(current_directory, start_file)
    if not os.path.exists(start_file__directory):
        with open(start_file__directory, 'w') as f:
            f.write('')  # creating an empty markdown file
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

            f.write('*.flv\n*.mp4\n*.srt\n*.vtt\n')
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
    files = [f for f in os.listdir(
        path) if os.path.isfile(os.path.join(path, f))]
    # r"How Ultrasonic Energy is Created _ Science of Energy Ep. 1 _ Ethicon-Bd2xISKVyFc.mp4"
    r"Monopolar Electrosurgery Technology and Principles - Science of Energy Ep. 5 - E.en.srt"
    reg_string_vid1 = [
        r'(.+) ｜ Understanding PID Control, Part (\d{1,2})\.mp4', '']
    reg_string_sub1 = [
        r"(.+) ｜ Understanding PID Control, Part (\d{1,2})\.en\.srt", r'\1']
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
            reg_string_sub_replace = series_num+"_"+r"\1"+r".en.srt"
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
