import pyperclip
import re
import os


def format_code_2_gpt_input(content=None, copy_to_clipboard=True):
    """
    Formats the input content by replacing multiple newline characters with a single newline character and
    multiple spaces with a single space. If no content is provided, it fetches the content from the clipboard,
    formats it, and then copies the formatted content back to the clipboard if copy_to_clipboard is True.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
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

    replacements = [
        (r"\n{2,}", "\n"),
        (r"[ ]{2,}", " ")
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)


def format_python_2_gpt_input(content=None, copy_to_clipboard=True):
    """
    Formats the input content by replacing multiple newline characters with a single newline character and
    multiple spaces with a single space. If no content is provided, it fetches the content from the clipboard,
    formats it, and then copies the formatted content back to the clipboard if copy_to_clipboard is True.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
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

    replacements = [
        (r"\n{2,}", "\n"),
        (r"[ ]{4}", "\t")
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)


def format_c_cpp_2_gpt_input(content=None, copy_to_clipboard=True):
    """
    Formats the input content by replacing multiple newline characters with a single newline character and
    multiple spaces with a single space. If no content is provided, it fetches the content from the clipboard,
    formats it, and then copies the formatted content back to the clipboard if copy_to_clipboard is True.

    :param content: The input content to format. If None, the content will be taken from the clipboard.
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

    replacements = [
        (r"\n{2,}", "\n"),
        (r"[ ]{2,}", " ")
    ]

    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)

    if copy_to_clipboard:
        try:
            pyperclip.copy(repr(content))
        except pyperclip.PyperclipException:
            print("Unable to copy content to the clipboard.")

    return repr(content)


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


def format_code_current_dir(current_dir=None):

    if current_dir is None:
        current_dir = os.getcwd()

    output_dir = os.path.join(current_dir, 'gpt_ready_code')
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, '.gitignore'), 'w', encoding="utf-8") as f:
        f.write("*_gpt.md\n")
    for root, dirs, files in os.walk(current_dir):
        for file in files:
            if file.endswith('.c') or file.endswith('.cpp') or file.endswith('.h') or file.endswith('.hpp') or file.endswith('.ahk') or file.endswith('.ini') or file.endswith('.py'):
                # Get file name
                file_name = os.path.basename(file)

                # Get directory name
                dir_name = os.path.basename(root)
                # print(dir_name)
                if dir_name.startswith('.'):
                    continue
                origin_dir = os.path.join(root, file)
                # read file skip none utf-8
                with open(origin_dir, 'r', encoding="utf-8") as f:
                    content = f.read()
                # content = read_file_skip_non_utf8_parts(origin_dir)

                content = format_python_2_gpt_input(
                    content=content, copy_to_clipboard=False) if file.endswith('.py') else format_c_cpp_2_gpt_input(content, copy_to_clipboard=False)
                floder_sep = os.path.join(output_dir, dir_name)
                os.makedirs(floder_sep, exist_ok=True)
                file_dir = os.path.join(floder_sep, f'{file_name}_gpt.md')
                total_dir = os.path.join(
                    output_dir, f'{dir_name}_gpt.md')

                with open(file_dir, 'w', encoding="utf-8") as f1:
                    f1.write(f"\"{file_name}\": \"{content}\",\n")
                if os.path.exists(total_dir):
                    with open(total_dir, 'r', encoding="utf-8") as f1:
                        content1 = f1.read()
                else:
                    content1 = ''
                with open(total_dir, 'w', encoding="utf-8") as f1:
                    content = f1.write(
                        content1+f"\"{file_name}\": \"{content}\",\n")

    return current_dir
