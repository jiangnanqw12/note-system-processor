import os
import re


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
