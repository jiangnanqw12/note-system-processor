import os
import re
import file_operations_utils
import pyperclip
import flags_utils
import shutil
import prompts
import urllib.parse


def srt_format_4_gpt(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()
    files_srt = [f for f in os.listdir(directory_path) if f.endswith('.srt')]
    for file in files_srt:
        with open(os.path.join(directory_path, file), "r", encoding="utf-8") as f1:
            lines = f1.readlines()

        content = ''

        for line in lines:
            line_temp = line.strip()
            content += line_temp

        reg_srt_2_gpt1 = [
            r'\d{1,3}\d{2}:(\d{2}:\d{2}),\d{3} --> \d{1,2}:\d{2}:\d{2},\d{3}', r'\n(\1) ']
        reg_srt_2_gpt = reg_srt_2_gpt1
        content = re.sub(reg_srt_2_gpt[0], reg_srt_2_gpt[1], content)
        with open(os.path.join(directory_path, file), "w", encoding="utf-8") as f1:
            f1.write(content)
    if files_srt != []:
        print(files_srt)
        prompts.video_summarization_expert_one(content)


def vtt_format_4_gpt(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()
    files_srt = [f for f in os.listdir(directory_path) if f.endswith('.vtt')]
    for file in files_srt:
        with open(os.path.join(directory_path, file), "r", encoding="utf-8") as f1:
            lines = f1.readlines()

        content = ''

        for line in lines:

            content += line.strip()+" "
        reg_vtt_2_gpt_list = []

        reg_vtt_2_gpt_list.append([
            r'\d{2}:(\d{2}:\d{2}).\d{3} --> \d{1,2}:\d{2}:\d{2}.\d{3}', r'\n(\1)'])
        reg_vtt_2_gpt_list.append([
            r'WEBVTT Kind:.+ Language:.+\n', r''])
        reg_vtt_2_gpt_list.append([r'&nbsp;', r' '])
        reg_vtt_2_gpt_list.append([r' line:\d{1,3}%', r' '])
        reg_vtt_2_gpt_list.append([r'[ ]{1,}', r' '])
        for reg_vtt_2_gpt in reg_vtt_2_gpt_list:

            content = re.sub(reg_vtt_2_gpt[0], reg_vtt_2_gpt[1], content)
        with open(os.path.join(directory_path, file), "w", encoding="utf-8") as f1:
            f1.write(content)
    if files_srt != []:
        print(files_srt)
        prompts.video_summarization_expert_one(content)


def subtitles_format_for_gpt_input(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()
    vtt_format_4_gpt(directory_path)
    srt_format_4_gpt(directory_path)
    # files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    # reg_string_list = []

    # reg_srt_time = [
    #     r'\d{1,3}\n(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3})\n']
    # for file in files_md:
    #     with open(os.path.join(directory_path, file), "r", encoding="utf-8") as f1:
    #         lines = f1.readlines()
    #     for i, line in enumerate(lines):
    #         line = line.strip()
    # r'\d{1,3}\n(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3})\n(.+)\n(.+)\n\n'
    # reg_string1 = [
    #     r'\d{1,3}\n(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3})\n(.+)\n(.+)\n\n', r"[[\1],[\2],[\3]]"]
    # reg_string_list.extend([reg_string1])
    # reg_string2 = [
    #     r'\d{1,3}\n(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3})\n(.+)\n(.+)', r"[[\1],[\2],[\3]]"]
    # reg_string_list.extend([reg_string2])
    # reg_string2 = [
    #     r'\d{1,3}\n(\d{1,2}:\d{1,2}:\d{1,2},\d{1,3} --> \d{1,2}:\d{1,2}:\d{1,2},\d{1,3})\n(.+)', r"[[\1],[\2]]"]
    # reg_string_list.extend([reg_string2])
    # reg_string3 = [r'\n\n', r"\n"]
    # reg_string_list.extend([reg_string3])
    # file_operations_utils.perform_regex_replacement_on_files(
    #     reg_string_list, directory_path, files_md)


def initialize_vid_note_file_structure(current_dir=None):

    TR_MODE = 1
    # Get content from clipboard
    content = pyperclip.paste()
    reg_content_to_current_topic = [r"\d{1,3}_(.+)\.mp4", r"\1"]
    match = re.search(reg_content_to_current_topic[0], content)
    if match:
        current_topic = re.sub(
            reg_content_to_current_topic[0], reg_content_to_current_topic[1], content)
    else:
        reg_content_to_current_topic = [r"(.+)\.mp4", r"\1"]
        match = re.search(reg_content_to_current_topic[0], content)
        if match:
            current_topic = re.sub(
                reg_content_to_current_topic[0], reg_content_to_current_topic[1], content)
        else:
            current_topic = content
    if TR_MODE == 1:
        print("current_topic: ", current_topic)
    if current_dir is None:
        current_dir = os.getcwd()

    # Check for existing serial numbers (first three digits of filenames)
    serial_numbers = [f[:3] for f in os.listdir(current_dir) if os.path.isfile(
        os.path.join(current_dir, f)) and f[:3].isdigit()]

    # Generate filename
    if serial_numbers:
        max_serial_number = max(serial_numbers)

        note_file = str(int(max_serial_number) + 1).zfill(3) + \
            "_"+current_topic+".md"

    else:
        note_file = "001"+"_"+current_topic+".md"
    if TR_MODE == 1:
        print("note_file: ", note_file)

    # Add the filename to the current_dir
    note_file_path = os.path.join(current_dir, note_file)
    if not os.path.exists(note_file_path):

        with open(note_file_path, 'w') as f:
            f.write("")

    sub_topic1_to_sub_topicn_folder_list = []
    sub_topic1_to_sub_topicn_folder_list.append(note_file[:-3])
    # sub_topic1_to_sub_topicn_folder_list.append(os.path.basename(current_dir))

    note_assets_dir_path = file_operations_utils.get_note_assets_dir_path(
        sub_topic1_to_sub_topicn_folder_list, current_dir)
    if TR_MODE == 1:
        print("note_assets_dir_path: ", note_assets_dir_path)
    file_operations_utils.create_file_subtitle_summary_gpt_md(
        note_assets_dir_path)

    Topic, sub_topic1 = file_operations_utils.get_Topic_in_kg(TR_MODE)

    if Topic is None:
        raise ValueError("Topic is None")
    bvids_origin_topic_path = file_operations_utils.get_bvids_origin_topic_path(
        Topic, TR_MODE)
    flag_search_sub_topic1 = flags_utils.get_flag_search_sub_topic1_in_bvids_origin_topic_path()
    if flag_search_sub_topic1:
        dirs = [d for d in os.listdir(bvids_origin_topic_path) if os.path.isdir(
            os.path.join(bvids_origin_topic_path, d))]
        if TR_MODE:
            print("dirs:", dirs)
        reg_string = r"\d{1,3}_"+sub_topic1
        flag_find_sub_topic = False
        for dir in dirs:
            if re.match(reg_string, dir):
                bvids_origin_topic_path = os.path.join(
                    bvids_origin_topic_path, dir)
                flag_find_sub_topic = True
                break
        if not flag_find_sub_topic:
            raise Exception("sub topic not found")
    # if match copy to des
    files_subtitle = [f for f in os.listdir(
        bvids_origin_topic_path) if f.endswith('.srt') or f.endswith('.vtt')]
    if TR_MODE:
        print("files_subtitle:", files_subtitle)
    reg_sub_string_current_topic = [
        r'(\d{1,3}_|)'+current_topic+r'(\.en|\.eng|\.zh|\.cn|\.zho|\.chi|\.zh-Hans|\.zh-Hant|)(\.srt|\.vtt)', r'']

    flag_one_by_one = flags_utils.get_flag_one_by_one()
    for file_srt in files_subtitle:
        match = re.match(reg_sub_string_current_topic[0], file_srt)
        flag_find_match = False
        if match:

            flag_find_match = True
            if ((match.group(2) == ".en") or (match.group(2) == "")):
                # copy srt to note_assets_dir_path
                new_srt_name = note_file[:-3]+match.group(2)+match.group(3)
                src_srt_file_path = os.path.join(
                    bvids_origin_topic_path, file_srt)
                des_srt_file_path = os.path.join(
                    note_assets_dir_path, new_srt_name)
                shutil.copy(src_srt_file_path, des_srt_file_path)
    if not flag_find_match:
        if flag_one_by_one:
            file_srt = files_subtitle[0]

            src_srt_file_path = os.path.join(
                bvids_origin_topic_path, file_srt)
            des_srt_file_path = os.path.join(
                note_assets_dir_path, file_srt)
            shutil.copy(src_srt_file_path, des_srt_file_path)

    subtitles_format_for_gpt_input(note_assets_dir_path)
    # todo generate prompt


def move_origin_vid_to_destination(TR_MODE=0):

    flag_one_by_one = flags_utils.get_flag_one_by_one()
    if TR_MODE:
        print("flag_one_by_one:", flag_one_by_one)
    flag_search_sub_topic1 = flags_utils.get_flag_search_sub_topic1_in_bvids_origin_topic_path()
    key_word, key_word_path = file_operations_utils.get_kg_bassets_folder_keyword()
    sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = file_operations_utils.get_bassets_keyword_path(
        key_word=key_word)
    # sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = get_bassets_keyword_path(key_word="NN_1687967434")
    origin_current_vid_file_name = ""
    # sub_topic1_to_sub_topicn_folder_list, OneDrive_KG_note_root_directory_path = get_kg_assets_root()
    Topic, sub_topic1, current_topic = file_operations_utils.get_Topic_in_kg_assets(
        TR_MODE)

    if TR_MODE:
        print("Folder list:", sub_topic1_to_sub_topicn_folder_list)
        print("OneDrive KG root directory_path:",
              OneDrive_KG_note_root_directory_path)

    BaiduSyncdisk_KG_note_root_directory_path = file_operations_utils.get_b_KG_directory_path(
        OneDrive_KG_note_root_directory_path)
    if TR_MODE:
        print("BaiduSyncdisk assets root _directory_path:",
              BaiduSyncdisk_KG_note_root_directory_path)

    bvids_origin_topic_path = file_operations_utils.get_bvids_origin_topic_path(
        Topic, TR_MODE=TR_MODE)

    if flag_search_sub_topic1:
        dirs = [d for d in os.listdir(bvids_origin_topic_path) if os.path.isdir(
            os.path.join(bvids_origin_topic_path, d))]
        if TR_MODE:
            print("dirs:", dirs)
        reg_string = r"\d{1,3}_"+sub_topic1
        flag_find_sub_topic = False
        for dir in dirs:
            if re.match(reg_string, dir):
                bvids_origin_topic_path = os.path.join(
                    bvids_origin_topic_path, dir)
                flag_find_sub_topic = True
                break
        if not flag_find_sub_topic:
            raise Exception("sub topic not found")
    files = [f for f in os.listdir(bvids_origin_topic_path) if os.path.isfile(
        os.path.join(bvids_origin_topic_path, f)) and f.endswith(".mp4")]
    files.sort()
    if TR_MODE:
        print("Files:", files)
    OneDrive_KG_current_note_directory_path = file_operations_utils.get_OneDrive_KG_note_path(
        OneDrive_KG_note_root_directory_path, sub_topic1_to_sub_topicn_folder_list)

    if TR_MODE:
        print("OneDrive KG note directory_path:",
              OneDrive_KG_current_note_directory_path)
    current_bvid_name = file_operations_utils.get_current_bvid_name()
    if TR_MODE:
        print("current_bvid_name:", current_bvid_name)
    serial_number = current_bvid_name[:3]
    if TR_MODE:
        print("serial_number:", serial_number)
    bvids_destination_directory_path = file_operations_utils.get_bvids_destination_long(
        sub_topic1_to_sub_topicn_folder_list, BaiduSyncdisk_KG_note_root_directory_path)
    if TR_MODE:
        print("bvids_destination_directory_path:",
              bvids_destination_directory_path)
    # bvid_reg_string = r'.+\(P\d{1,3}\. \d{1,3}\.\d{1,3}\.\d{1,3}(.+)\)\.mp4'

    current_bvid_destination_file_path = os.path.join(
        bvids_destination_directory_path, current_bvid_name)
    if flag_one_by_one:

        if not os.path.exists(current_bvid_destination_file_path):
            vid_name_origin = files[0]
        # origin_current_vid_file_name = "\n"+re.sub(bvid_reg_string, r'\1', vid_name_origin)
            origin_current_vid_file_name = vid_name_origin
            os.rename(os.path.join(bvids_origin_topic_path,
                      vid_name_origin), current_bvid_destination_file_path)
            reg_string_sub = r"^"+vid_name_origin[:-4]+r"(\..+|)(\.srt|\.vtt)$"
            files_sub = [f for f in os.listdir(bvids_origin_topic_path) if os.path.isfile(
                os.path.join(bvids_origin_topic_path, f)) and (f.endswith(".srt") or f.endswith(".vtt"))]

            for file_sub in files_sub:
                match = re.search(reg_string_sub, file_sub)

                if match:

                    os.rename(os.path.join(
                        bvids_origin_topic_path, file_sub), os.path.join(bvids_destination_directory_path, file_sub))

        # current_bsrt_name = current_bvid_name[:-4]+".srt"
        # if TR_MODE:
        #     print("current_bsrt_name:", current_bsrt_name)
        # current_bsrt_name_en = current_bvid_name[:-4]+".en.srt"
        # if TR_MODE:
        #     print("current_bsrt_name_en:", current_bsrt_name_en)
        # current_bsrt_file_path = os.path.join(
        #     bvids_destination_directory_path, current_bsrt_name)
        # current_bsrt_file_path_en = os.path.join(
        #     bvids_destination_directory_path, current_bsrt_name_en)
        # if (not os.path.exists(current_bsrt_file_path)) and (not os.path.exists(current_bsrt_file_path_en)):

        #     srt_name_front = vid_name_origin[:-4]

        #     reg_string_srt = r"^"+srt_name_front+r"(.+)\.srt$"

        #     for file_srt in files_sub:
        #         match = re.search(reg_string_srt, file_srt)
        #         if match:
        #             srt_name_origin = file_srt

        #             new_srt_name = current_bvid_name[:-4]+match.group(1)+".srt"
        #             if TR_MODE:
        #                 print("srt_name_origin:", srt_name_origin)
        #                 print("new_srt_name:", new_srt_name)
        #             new_srt_file_path = os.path.join(
        #                 bvids_destination_directory_path, new_srt_name)
        #             os.rename(os.path.join(
        #                 bvids_origin_topic_path, srt_name_origin), new_srt_file_path)
        #         else:
        #             reg_string_srt2 = r"^"+srt_name_front+r"\.srt$"
        #             match = re.search(reg_string_srt2, file_srt)
        #             if match:
        #                 srt_name_origin = file_srt

        #                 new_srt_name = current_bvid_name[:-4]+".srt"
        #                 if TR_MODE:
        #                     print("srt_name_origin:", srt_name_origin)
        #                     print("new_srt_name:", new_srt_name)
        #                 new_srt_file_path = os.path.join(
        #                     bvids_destination_directory_path, new_srt_name)
        #                 os.rename(os.path.join(
        #                     bvids_origin_topic_path, srt_name_origin), new_srt_file_path)

    # else:
    #     bvid_reg_string, bvid_srt_reg_string = get_bvid_reg_string(
    #         sub_topic1_to_sub_topicn_folder_list, TR_MODE)
    #     flag_match = 0
    #     for file in files:
    #         match = re.search(bvid_reg_string, file)
    #         if match:
    #             flag_match = 1
    #             vid_name_origin = file
    #             if TR_MODE:
    #                 print("vid_name_origin:", vid_name_origin)
    #                 print(match.group(0))
    #             break

    #     if flag_match == 0 and (not os.path.exists(current_bvid_destination_file_path)):
    #         raise ValueError("No match found.")
    #     if not os.path.exists(current_bvid_destination_file_path):

    #         os.rename(os.path.join(bvids_origin_topic_path,
    #                   vid_name_origin), current_bvid_destination_file_path)

    #     files_srt = [f for f in os.listdir(bvids_origin_topic_path) if os.path.isfile(
    #         os.path.join(bvids_origin_topic_path, f)) and f.endswith(".srt")]
    #     for file_srt in files_srt:
    #         match = re.search(bvid_srt_reg_string, file_srt)
    #         if match:
    #             new_srt_name = current_bvid_name[:-4]+".srt"
    #             new_srt_path = os.path.join(
    #                 bvids_destination_directory_path, new_srt_name)
    #             if not os.path.exists(new_srt_path):
    #                 os.rename(os.path.join(
    #                     bvids_origin_topic_path, file_srt), new_srt_path)
    return origin_current_vid_file_name, current_bvid_destination_file_path, OneDrive_KG_current_note_directory_path


def vid_path_2_md_vid_link(vid_path, current_bvid_name):
    import urllib
    url_path = urllib.parse.quote(os.path.abspath(vid_path))
    url = "file:///" + url_path.replace("\\", "/")
    md_show_url = f"![{current_bvid_name}]({url})"
    md_url = f"[{current_bvid_name}]({url})"
    return md_show_url, md_url


def convert_chatgpt_summary_text_to_one_line_summary(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []
    reg_string1 = [
        r'(Section \d{1,2}: |Title: )(.+)\n{1,2}(Start|Start Timestamp): (|\()(\d{1,2}:\d{1,2})(|\))\n{1,2}Summary(: |:\n)(.+)', r"- \2 (\5) \8"]
    reg_string_list.append(reg_string1)
    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def check_video_file_path_conforms_to_pattern(str_url):
    r"![001_Derivatives of multivariable functions.mp4](file:///C%3A%5CBaiduSyncdisk%5Cassets%5CO%5CO1%5CO17%5CO172%5CMultivaribale_calculus_Khan_Academy%5Cassets%5Cbvids%5Cmc_1683793602%5C002%5C001%5C001_Derivatives%20of%20multivariable%20functions.mp4)"
    url_pattern_4_file_vid = r'(!\[.+\..+\]\(file:///C:%5CBaiduSyncdisk%5Cassets(%5C.+){1,}\.\w+)(\))'
    url_pattern_4_file_vid2 = r'(!\[.+\..+\]\(file:///C%3A%5CBaiduSyncdisk%5Cassets(%5C.+){1,}\.\w+)(\))'
    match1 = re.search(url_pattern_4_file_vid, str_url)
    if not match1:
        match1 = re.search(url_pattern_4_file_vid2, str_url)
        if not match1:
            print("str_url: ", str_url)
            raise Exception('No match found')
    return match1


def convert_min_sec_to_seconds(time_str):
    time_line_pattern_str = r'\((\d{1,2}:\d{1,2})-(\d{1,2}:\d{1,2})\)[ ]{1,}'
    time_stamp_pattern_str = r'(\d{1,2}):(\d{1,2})'
    match = re.search(time_line_pattern_str, time_str)
    if match:
        time_line_start = match.group(1)
        time_line_end = match.group(2)
        time_line_start_seconds = int(time_line_start.split(
            ':')[0])*60+int(time_line_start.split(':')[1])
        return time_line_start_seconds
    else:
        match = re.search(time_stamp_pattern_str, time_str)
        if match:
            time_seconds = int(match.group(1)) * 60 + int(match.group(2))
            return time_seconds
        else:
            return None


def get_list_time_head_textshort_text_4_file(file, key_word):
    # print("start to generate time line for video and head text:")

    number_list_head_time_text_pattern_str = r'((\d{1,2}\.)|-)[ ]{1,}(.+) \((\d{1,2}):(\d{1,2})\) (.+)'
    number_list_head_time_pattern_str = r'(\d{1,2}):(\d{1,2}) - (.+)'
    number_list_head_time_pattern_str2 = r'(\d{1,2}):(\d{1,2}) (.+)'
    time_text_pattern_str = r'\((\d{1,2}):(\d{1,2})\)[ ]{0,}([^\n]+)[\n]{0,}'

    pattern_dict = dict()
    pattern_dict["timestamps"] = number_list_head_time_pattern_str
    pattern_dict["summary_gpt"] = number_list_head_time_text_pattern_str
    pattern_dict["subtitle"] = time_text_pattern_str
    list_time_head_textshort_text = []
    with open(os.path.join(os.getcwd(), file), 'r', encoding='UTF-8') as f:
        lines = f.readlines()

    for line in lines:
        time_line_start_seconds = convert_min_sec_to_seconds(line)
        if time_line_start_seconds != None:
            if key_word in pattern_dict:
                pattern_str = pattern_dict[key_word]
                match = re.search(pattern_str, line)
                if match:
                    if key_word == "timestamps":
                        list_time_head_textshort_text.append(
                            [time_line_start_seconds, match.group(3), None, None])
                    elif key_word == "summary_gpt":
                        # for i in range(len(match.groups())):
                        #     print(i,match.group(i))
                        list_time_head_textshort_text.append(
                            [time_line_start_seconds, match.group(3), match.group(6), None])
                    elif key_word == "subtitle":
                        list_time_head_textshort_text.append(
                            [time_line_start_seconds, None, None, match.group(3)])
                else:
                    if key_word == "timestamps":
                        match2 = re.search(
                            number_list_head_time_pattern_str2, line)
                        if match2:
                            list_time_head_textshort_text.append(
                                [time_line_start_seconds, match2.group(3), None, None])
                        else:
                            print("no match for line:", line)
                            print(key_word)
                    else:
                        print("no match for line:", line)
                        print(key_word)
            else:
                raise Exception("key_word not in pattern_dict")

    # print("List of time, heading, short text, text:")
    # print(list_time_head_textshort_text)
    return list_time_head_textshort_text


def list_time_head_textshort_text_to_vid_timeline_md(timeline_data, file, match):
    # print(timeline_data)
    assets_root_path, assets_root_dir = file_operations_utils.get_assets_root_path()
    output_dir = file_operations_utils.create_output_directory(
        assets_root_path)
    new_file_name = file_operations_utils.create_new_file_name(file)
    flag_write_line_by_line = True
    if not flag_write_line_by_line:
        content = ""

    with open(os.path.join(output_dir, new_file_name), 'w', encoding='UTF-8') as f:
        for i, (start_time, heading, short_text, text) in enumerate(timeline_data):
            start_time_sec = int(start_time)

            if i == len(timeline_data) - 1:
                end_time_sec = start_time_sec + 999
            else:
                end_time_sec = int(timeline_data[i + 1][0])

            if heading:
                if flag_write_line_by_line:
                    f.write(f"## {heading}\n\n")
                else:
                    content += f"## {heading}\n\n"

                i_temp = i
                flag_find_next_head = False
                while i_temp < len(timeline_data) - 1:
                    i_temp += 1
                    if timeline_data[i_temp][1]:
                        end_time_sec2 = int(timeline_data[i_temp][0])
                        vid_line = f"{match.group(1)}#t={start_time_sec},{end_time_sec2}{match.group(3)}"
                        if flag_write_line_by_line:
                            f.write(f"{vid_line}\n\n")
                        else:
                            content += f"{vid_line}\n\n"
                        flag_find_next_head = True
                        break

                if not flag_find_next_head:
                    vid_line = f"{match.group(1)}#t={start_time_sec}{match.group(3)}"
                    if flag_write_line_by_line:
                        f.write(f"{vid_line}\n\n")
                    else:
                        content += f"{vid_line}\n\n"

            if short_text:
                if flag_write_line_by_line:
                    f.write(f"- {short_text}\n\n")
                else:
                    content += f"- {short_text}\n\n"
            if heading:
                if flag_write_line_by_line:
                    f.write(f"---\n\n\n\n")
                else:
                    content += f"---\n\n\n\n"
            if text:
                vid_line = f"{match.group(1)}#t={start_time_sec},{end_time_sec}{match.group(3)}"
                if flag_write_line_by_line:
                    f.write(f"{vid_line}\n\n")
                    f.write(f"{text}\n\n")
                else:
                    content += f"{vid_line}\n\n"
                    content += f"{text}\n\n"
            if flag_write_line_by_line:
                pass
            else:
                f.write(content)
                content = ""
    return output_dir, new_file_name


def convert_md_vid_link_to_html(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_string2 = [r'(!\[\]|!\[.+\])\((file:///.+(\.mp4|\.mp4#t=.+))\)',
                   r'<video src="\2" controls></video>']
    reg_string_list.extend([reg_string2])

    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def convert_md_vid_link_to_html_tree(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    reg_string_list = []

    reg_string2 = [r'(!\[\]|!\[.+\])\((file:///.+(\.mp4|\.mp4#t=.+))\)',
                   r'<video src="\2" controls></video>']
    reg_string_list.extend([reg_string2])

    perform_regex_replacement_on_files_tree(reg_string_list, directory_path)


def convert_gpt_summary_to_markdown_vid_timeline(str_url, TR_MODE, path=None):

    # str_url=r'![009_area-and-slope.mp4](file:///C:%5CBaiduSyncdisk%5Cassets%5CO%5CO1%5CO17%5CO172%5CCalculus%203Blue1Brown%5Cassets%5Cbvids%5C009_area-and-slope.mp4)'

    match1 = check_video_file_path_conforms_to_pattern(str_url)

    if path is None:
        path = os.getcwd()
    file_list = os.listdir(path)
    assets_root_path, assets_root_dir = file_operations_utils.get_assets_root_path()
    if TR_MODE:
        print("assets_root_path is : ", assets_root_path)
    output_dir = file_operations_utils.create_output_directory(
        assets_root_path)
    if TR_MODE:
        print("output_dir is : ", output_dir)
    for file in file_list:
        if file.endswith(".md"):

            if file.find("summary_gpt") != -1:
                cwd_floder_name = os.path.basename(path)
                file_summary = file
                key_word = "summary_gpt"
                list_time_head_textshort = get_list_time_head_textshort_text_4_file(
                    file, key_word)
                # list_time_head_textshort_text_to_vid_timeline_md(list_time_head_textshort_text,file,match1)
    if TR_MODE:
        print("list_time_head_textshort is :", list_time_head_textshort)
    list_time_head_textshort_text_to_vid_timeline_md(
        list_time_head_textshort, file_summary, match1)
    convert_md_vid_link_to_html(output_dir)
    return output_dir, file_summary


def get_note_vid_name():
    file = os.path.basename(os.getcwd())
    return file+r'_vid'+".md"


def merge_all_content_into_md_note_file(note_name, file_summary_path, origin_current_vid_file_name, current_vid_md_link_content, OneDrive_KG_current_note_directory_path):
    with open(os.path.join(OneDrive_KG_current_note_directory_path, note_name), "r", encoding="utf-8") as f:
        current_note_origin_content = f.read()
    with open(file_summary_path, "r", encoding="utf-8") as f:
        current_vid_summary = f.read()
    with open(os.path.join(OneDrive_KG_current_note_directory_path, note_name), "w", encoding="utf-8") as f:
        f.write(current_note_origin_content+origin_current_vid_file_name +
                current_vid_md_link_content+current_vid_summary)


def generate_vid_note_with_timeline_from_text_summary():
    TR_MODE = 1

    origin_current_vid_file_name, current_bvid_destination_file_path, OneDrive_KG_current_note_directory_path = move_origin_vid_to_destination(
        TR_MODE)
    current_bvid_name = file_operations_utils.get_current_bvid_name()
    if TR_MODE:
        print("current_bvid_name:", current_bvid_name)

    md_show_url, md_url = vid_path_2_md_vid_link(
        current_bvid_destination_file_path, current_bvid_name)
    current_vid_md_link_content = '\n\n'+md_url+'\n'+md_show_url+'\n\n'
    if TR_MODE:
        print("md_show_url:", md_show_url)
        print("md_url:", md_url)
    convert_chatgpt_summary_text_to_one_line_summary()
    # output_dir, file_summary = convert_subtitle_and_summary_to_markdown_vid_timeline(
    #     md_show_url)
    output_dir, file_summary = convert_gpt_summary_to_markdown_vid_timeline(
        md_show_url, TR_MODE)
    file_summary_path = os.path.join(output_dir, file_summary)
    note_name = get_note_vid_name()
    if TR_MODE:
        print("note_name:", note_name)
    if not os.path.exists(os.path.join(OneDrive_KG_current_note_directory_path, note_name)):
        # print(os.path.join(OneDrive_KG_current_note_directory_path, note_name),"is note exists")
        # raise Exception("note not found")
        with open(os.path.join(OneDrive_KG_current_note_directory_path, note_name), "w", encoding="utf-8") as f:
            pass

    merge_all_content_into_md_note_file(note_name, file_summary_path, origin_current_vid_file_name,
                                        current_vid_md_link_content, OneDrive_KG_current_note_directory_path)
    convert_md_vid_link_to_html(OneDrive_KG_current_note_directory_path)


def timestamps_3blue1brown_2_timeline(str_url):
    # process url
    # str_url=r'![007_limits.mp4](file:///C:%5CBaiduSyncdisk%5Cassets%5CO%5CO1%5CO17%5CO172%5CCalculus%203Blue1Brown%5Cassets%5Cbvids%5C007_limits.mp4)'
    # '(!\[.+\..+\]\(file:///C:%5CBaiduSyncdisk%5Cassets(%5C.+){1,}\.\w+)(\))'
    match1 = check_video_file_path_conforms_to_pattern(str_url)
    # timestamps file
    file_list = os.listdir(os.getcwd())
    for file in file_list:
        if file.endswith(".md") or file.endswith(".txt"):
            if file.find("timestamps") != -1:
                key_word = "timestamps"
                list_time_head_textshort_text = get_list_time_head_textshort_text_4_file(
                    file, key_word)

                output_dir, file_name = list_time_head_textshort_text_to_vid_timeline_md(
                    list_time_head_textshort_text, file, match1)

                return output_dir, file_name


def generate_vid_note_with_timeline_from_timestamps():
    TR_MODE = 1

    origin_current_vid_file_name, current_bvid_destination_file_path, OneDrive_KG_current_note_directory_path = move_origin_vid_to_destination(
        TR_MODE)
    current_bvid_name = file_operations_utils.get_current_bvid_name(
        current_bvid_destination_file_path)
    md_show_url, md_url = vid_path_2_md_vid_link(
        current_bvid_destination_file_path, current_bvid_name)
    current_vid_md_link_content = '\n\n'+md_url+'\n'+md_show_url+'\n\n'
    if TR_MODE:
        print("md_show_url:", md_show_url)
        print("md_url:", md_url)

    output_dir, file_summary = timestamps_3blue1brown_2_timeline(md_show_url)
    file_summary_path = os.path.join(output_dir, file_summary)
    note_name = get_note_vid_name()
    if TR_MODE:
        print("note_name:", note_name)
    if not os.path.exists(os.path.join(OneDrive_KG_current_note_directory_path, note_name)):
        # print(os.path.join(OneDrive_KG_current_note_directory_path, note_name),"is note exists")
        # raise Exception("note not found")
        with open(os.path.join(OneDrive_KG_current_note_directory_path, note_name), "w", encoding="utf-8") as f:
            pass
    merge_all_content_into_md_note_file(note_name, file_summary_path, origin_current_vid_file_name,
                                        current_vid_md_link_content, OneDrive_KG_current_note_directory_path)

    convert_md_vid_link_to_html(OneDrive_KG_current_note_directory_path)


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
