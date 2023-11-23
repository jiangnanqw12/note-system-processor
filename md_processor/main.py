#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse


def test():
    pass


def md_note_process(num=0, head_num=1):
    import md_helper
    import html_processor
    operations = {
        1: md_helper.remove_back_matter_and_copy_code,
        2: md_helper.process_md_head_to_hn,
        3: md_helper.retrieve_document_summary_info,
        4: md_helper.format_text_for_markdown,
        5: md_helper.create_file_based_on_content,
        6: md_helper.format_2_gpt_input,
        7: md_helper.mermaid_format,
        8: html_processor.convert_html_to_md,
        9: html_processor.change_html_title,
        10: md_helper.create_node_for_mermaid,


    }

    if num in operations:
        if (num == 2):
            operations[num](head_num)
        else:
            operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def wiki_note_process(num=0):
    import wiki_processor
    operations = {
        1: wiki_processor.remove_wiki_edit_link,
        2: wiki_processor.remove_wiki_equation_svg,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def book_processor(num=0):
    import book_processor
    operations = {
        1: book_processor.perform_regex_replacement_on_index_file,

        2: book_processor.perform_regex_replacement_on_zhi_book_mds_name,
        3: book_processor.rename_files_base_on_index_markdown,
        4: book_processor.prepend_filename_as_header_if_chapter_present,
        5: book_processor.lower_header_level_in_md_files,

        6: book_processor.remove_md_copy_code,
        7: book_processor.perform_regex_replacement_on_zhi_mds,
        8: book_processor.convert_zhi_footnote_to_obsidian,
        10: book_processor.merge_all_md_files_into_one,
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


def vid_note_process(num=0):
    import vid_note_processor
    operations = {
        1: vid_note_processor.initialize_vid_note_file_structure,
        2: vid_note_processor.generate_vid_note_with_timeline_from_text_summary,
        3: vid_note_processor.generate_vid_note_with_timeline_from_timestamps,
        4: vid_note_processor.convert_md_vid_link_to_html,
        5: vid_note_processor.convert_md_vid_link_to_html_tree,
        6: vid_note_processor.vtt_format_4_gpt,
        7: vid_note_processor.mul_initialize_vid_note_file_structure,


    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def os_file_processor(num=0):
    import file_operations_utils
    import markmind
    operations = {
        1: file_operations_utils.initialize_notes_files_structure,
        2: file_operations_utils.add_timestamp_to_filenames,
        3: file_operations_utils.get_current_timestamp,
        4: file_operations_utils.open_b_assets_folder,
        5: file_operations_utils.rename_folders_4_mooc_b,
        6: file_operations_utils.create_drawio_file_based_on_content,
        7: file_operations_utils.create_excalidraw_file_based_on_content,
        8: file_operations_utils.rename_index_folder_files,
        9: file_operations_utils.rename_bilibili_subs,
        10: markmind.create_annotator,
        11: file_operations_utils.rename_files_in_directories,



    }

    if num in operations:
        operations[num]()
    elif num == 0:
        print("Available operations:")
        for num, func in operations.items():
            print(f"{num}: {func.__name__}")
    else:
        raise ValueError("Invalid operation number.")


def get_prompts(num=0):
    import prompt_generator
    operations = {
        1: prompt_generator.video_summarization_expert_one,
        2: prompt_generator.get_prompt_explain_c_cpp,
        3: prompt_generator.chatbot_prompt_expert,
        4: prompt_generator.Translate_Chinese_sentence_into_function_name,
        5: prompt_generator.Expert_Prompt_Creator,
        6: prompt_generator.dot2mermaid,
        7: prompt_generator.code_improve,
        8: prompt_generator.format_code_current_dir,


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
    parser.add_argument('-i', '--input_int', type=int, default=r'0',
                        help='input input_int to pass to the function')
    parser.add_argument('-hn', '--head_num', type=int, default=r'1',
                        help='input head_num to pass to the function')

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

    parser.add_argument('-test', '--test',
                        action='store_true', help='call test')
    parser.add_argument('-bp', '--book_processor',
                        action='store_true', help='call book_processor')
    parser.add_argument('-ofp', '--os_file_processor',
                        action='store_true', help='call os_file_processor')

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

    elif args.test:
        test(args.input_int)

    elif args.book_processor:
        book_processor(args.input_int)
    elif args.os_file_processor:
        os_file_processor(args.input_int)
    elif args.get_prompts:
        get_prompts(args.input_int)
    else:
        print("Invalid argument")


if __name__ == "__main__":
    main()
