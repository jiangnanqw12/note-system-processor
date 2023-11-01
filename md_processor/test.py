import os


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
