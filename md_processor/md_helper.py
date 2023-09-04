import pyperclip
import os
import re

import time


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

# def get_highest_head_level(content):
#     lines = content.split('\n')
#     highest_level = float('inf')
#     reg_string=[r"^(#{1,}) .+",r'\1']
#     for line in lines:
#         match=line.search(reg_string[0])
#         if match:
#             line.count("#")

#     return highest_level


def downgrade_heads(content, downgrade_level):
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
            new_head_level = head_level + downgrade_level
            if new_head_level > 6:
                new_head_level = 6
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
            content, head_number+1-highest_head_level)
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

    timestamp = str(int(time.time()))
    new_name = content.strip() + "_" + timestamp + ".md"

    with open(os.path.join(path, new_name), "w", encoding="utf-8") as file:
        file.write(content)


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
