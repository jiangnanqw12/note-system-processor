import pyperclip
import re
import os
import shutil

def format_code(content=None, level=1, copy_to_clipboard=True):
    """
    Formats the input content by applying different levels of formatting.
    
    Level 1: Replace multiple newlines with one newline.
    Level 2: Replace multiple newlines with one newline, and multiple spaces with one space.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
    :param level: The formatting level to apply (1 or 2).
    :param copy_to_clipboard: A flag indicating whether to copy the formatted content back to the clipboard.
    :return: The formatted content as a string.
    """
    if content is None:
        try:
            content = pyperclip.paste()
        except pyperclip.PyperclipException:
            print("Unable to access the clipboard.")
            return None

    content = content.replace("\r\n", "\n").replace("\\\\n", "\n")

    if level >= 1:
        content = re.sub(r"\n{2,}", "\n", content)

    if level >= 2:
        content = re.sub(r"[ ]{2,}", " ", content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)

def format_python_2_gpt_input(content=None, level=1, copy_to_clipboard=True):
    """
    Formats Python code with different levels of formatting.
    Level 1: Replace multiple newlines with one newline.
    Level 2: Replace multiple newlines with one newline, and replace 4 spaces with a tab.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
    :param level: The formatting level to apply (1 or 2).
    :param copy_to_clipboard: A flag indicating whether to copy the formatted content back to the clipboard.
    :return: The formatted content as a string.
    """
    if content is None:
        try:
            content = pyperclip.paste()
        except pyperclip.PyperclipException:
            print("Unable to access the clipboard.")
            return None

    content = content.replace("\r\n", "\n").replace("\\\\n", "\n")

    if level >= 1:
        content = re.sub(r"\n{2,}", "\n", content)

    if level >= 2:
        content = re.sub(r"[ ]{4}", "\t", content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)

def format_c_cpp_2_gpt_input(content=None, level=1, copy_to_clipboard=True):
    """
    Formats C/C++ code with different levels of formatting.
    Level 1: Replace multiple newlines with one newline.
    Level 2: Replace multiple newlines with one newline, and replace multiple spaces with one space.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
    :param level: The formatting level to apply (1 or 2).
    :param copy_to_clipboard: A flag indicating whether to copy the formatted content back to the clipboard.
    :return: The formatted content as a string.
    """
    return format_code(content=content, level=level, copy_to_clipboard=copy_to_clipboard)

def read_file_skip_non_utf8_parts(file_path):
    import logging
    """
    Reads a file in binary mode and decodes it to UTF-8.
    Skips the parts of the file that are not UTF-8 encoded.

    :param file_path: Path to the file.
    :return: Decoded file content with non-UTF-8 parts skipped.
    """
    try:
        with open(file_path, 'rb') as f:
            byte_content = f.read()
            return byte_content.decode('utf-8', errors='ignore')
    except Exception as e:
        logging.error(f"Error reading file {file_path}: {e}")
    return None

def format_code_current_dir(current_dir=None, level=2):
    if current_dir is None:
        current_dir = os.getcwd()
    output_dir = os.path.join(current_dir, 'format_code')
    
    # Check if output_dir exists; if yes, clear its contents
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # Remove all contents in the directory
    
    os.makedirs(output_dir, exist_ok=True)  # Create a fresh output_dir
    
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(('.c', '.cpp', '.h', '.hpp', '.ahk', '.ini', '.py')):
                file_name = os.path.basename(file)
                dir_name = os.path.basename(root)
                if dir_name.startswith('.'):
                    continue
                origin_dir = os.path.join(root, file)
                with open(origin_dir, 'r', encoding="utf-8") as f:
                    content = f.read()
                if file.endswith('.py'):
                    content = format_python_2_gpt_input(content=content, level=level, copy_to_clipboard=False)
                else:
                    content = format_c_cpp_2_gpt_input(content=content, level=level, copy_to_clipboard=False)
                folder_sep = os.path.join(output_dir, dir_name)
                os.makedirs(folder_sep, exist_ok=True)
                file_dir = os.path.join(folder_sep, f'{file_name}_formated.md')
                total_dir = os.path.join(output_dir, f'{dir_name}_formated.md')
                with open(file_dir, 'w', encoding="utf-8") as f1:
                    f1.write(f'"{file_name}": "{content}",\n')
                if os.path.exists(total_dir):
                    with open(total_dir, 'r', encoding="utf-8") as f1:
                        content1 = f1.read()
                else:
                    content1 = ''
                
                with open(total_dir, 'w', encoding="utf-8") as f1:
                    f1.write(content1 + f'"{file_name}": "{content}",\n')
    return current_dir


def get_all_code(current_dir=None):
    if current_dir is None:
        current_dir = os.getcwd()

    file_list = [".c", ".cpp", ".h", ".hpp", ".ahk", ".ini", ".py"]
    output_dir = os.path.join(current_dir, '_database_code')

    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, '.gitignore'), 'w', encoding="utf-8") as f:
        f.write("*\n")

    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith(tuple(file_list)):
                file_name = os.path.basename(file)
                dir_name = os.path.basename(root)
                if dir_name.startswith('_') or dir_name.startswith('.'):
                    continue

                origin_dir = os.path.join(root, file)
                output_dir_temp = os.path.join(output_dir, f"_{dir_name}")
                os.makedirs(output_dir_temp, exist_ok=True)
                output_dir_temp = os.path.join(output_dir_temp, file_name)

                import shutil
                shutil.copy(origin_dir, output_dir_temp)

    return current_dir
