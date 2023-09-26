import pyperclip
import os
import re

import time
import file_operations_utils


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


def remove_back_matter_and_copy_code(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_Back_matter_template = [r"---\n\n- created:.+\n- source: .+", r""]
    reg_string_list.extend([reg_Back_matter_template])
    reg_string_copy_code = [r"```\n(.+)Copy code", r"```\1\n"]
    reg_string_list.extend([reg_string_copy_code])
    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def Is_head_line(line):
    pattern = r"^(#{1,}) (.+|)"
    match = re.search(pattern, line)
    if match:
        return True
    else:
        return False


def get_highest_head_level(content):
    lines = content.split('\n')
    lowest_level = float('inf')
    pattern = re.compile(r"^(#{1,}) ")

    for line in lines:
        match = pattern.match(line)
        if match:
            level = len(match.group(1))
            if level < lowest_level:
                lowest_level = level

    return lowest_level if lowest_level != float('inf') else None


def downgrade_heads(content, downgrade_level):
    lines = content.split('\n')
    new_lines = []

    for line in lines:
        if Is_head_line(line):
            head_level = 0
            for char in line:
                if char == '#':
                    head_level += 1
                else:
                    break
            if head_level > 0:
                new_head_level = head_level + downgrade_level
                if new_head_level > 6:
                    new_head_level = 6
                new_line = '#' * new_head_level + line[head_level:]
                new_lines.append(new_line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def upgrade_heads(content, upgrade_level):
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        head_level = 0
        for char in line:
            if char == '#':
                head_level += 1
            else:
                break
        if head_level > 0:
            new_head_level = head_level - upgrade_level
            if new_head_level < 1:
                new_head_level = 1
            new_line = '#' * new_head_level + line[head_level:]
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


def degrade_markdown_by_head_number(head_number):

    content = pyperclip.paste()
    TR_MODE = 1
    highest_head_level = get_highest_head_level(content)
    # highest_head_level=3
    if TR_MODE:
        print("highest_head_level: ", highest_head_level)
        print("head_number: ", head_number)
    if highest_head_level < head_number:
        content = downgrade_heads(
            content, head_number-highest_head_level)
        pyperclip.copy(content)


def upgrade_markdown_by_head_number(head_number):
    content = pyperclip.paste()
    TR_MODE = 1
    highest_head_level = get_highest_head_level(content)

    if TR_MODE:
        print("highest_head_level: ", highest_head_level)
        print("head_number: ", head_number)

    if highest_head_level > head_number:
        content = upgrade_heads(
            content, highest_head_level-head_number)
        pyperclip.copy(content)


def process_md_head_to_hn(head_number, content=None):
    if content is None:
        content = pyperclip.paste()
    TR_MODE = 1
    highest_head_level = get_highest_head_level(content)

    if TR_MODE:
        print("highest_head_level: ", highest_head_level)
        print("head_number: ", head_number)

    if highest_head_level > head_number:
        content = upgrade_heads(
            content, highest_head_level-head_number)
        pyperclip.copy(content)
    elif highest_head_level < head_number:
        content = downgrade_heads(
            content, head_number-highest_head_level)
        pyperclip.copy(content)


def format_2_gpt_input(content=None):
    """
    This function formats the input content by replacing one or more newline characters with a single newline character.
    If no content is provided, it fetches the content from the clipboard, formats it, and then copies the formatted content back to the clipboard.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
    """
    if content is None:
        content = pyperclip.paste()

    print(repr(content))
    content = content.replace("\r\n", "\n")

    match = re.search(r"\n{2,}", content)
    if match:
        print("Match found: ", match.group())
        newline_pattern = re.compile(r"\n{2,}")
        # Replacing multiple newlines with a single newline
        content = newline_pattern.sub("\n", content)

    # Printing the formatted content
    print(repr(content))

    # Copying the formatted content back to the clipboard
    pyperclip.copy(content)


def retrieve_document_summary_info(content=None):
    if content is None:

        content = pyperclip.paste()
    reg_string1 = [
        r'(#{1,6}) (.+)\n\n<video src="file://.+" controls></video>\n\n- .+', r"\1# \2"]
    match = re.search(reg_string1[0], content)
    if match:
        content = re.sub(reg_string1[0], reg_string1[1], content)
    reg_string2 = [r'\n{3,}', r'\n\n']
    content = re.sub(reg_string2[0], reg_string2[1], content)
    pyperclip.copy(content)


def format_ocr_text(content=None):
    TR_mode = False
    if content is None:
        content = pyperclip.paste()
    if TR_mode:
        print(":", repr(content))

    content = content.replace('\n', ' ')
    content = content.replace('\r', ' ')
    if TR_mode:
        print(repr(content))

    while '  ' in content:
        content = content.replace('  ', ' ')
    if TR_mode:
        print(repr(content))
    pyperclip.copy(content)


def create_file_based_on_content(content=None, path=None):
    """
    This function creates a file based on the content provided.

    Parameters:
    content (str): The content to be written to the file. If not provided, it will use the content from the clipboard.
    path (str): The path where the file will be created. If not provided, it will use the current working directory.

    Raises:
    ValueError: If the length of the content is less than 1 or greater than 100.
    TypeError: If the content contains more than 2 newline characters.
    """

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
    new_name = content.strip() + "_" + timestamp + ".md"

    with open(os.path.join(path, new_name), "w", encoding="utf-8") as file:
        file.write("")


def main():
    content = pyperclip.paste()
    highest_level = get_highest_head_level(content)
    print(f"The highest head level is {highest_level}")
    downgrade_level = int(
        input("Enter the number by which you want to downgrade the headers: "))
    new_content = downgrade_heads(content, downgrade_level)
    pyperclip.copy(new_content)
    print("Content updated in clipboard.")


if __name__ == "__main__":
    main()
