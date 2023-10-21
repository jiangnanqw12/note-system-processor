import os
import re
import file_operations_utils

# epub


def base_on_mulu_rename_mds(path=None):
    if path is None:
        path = os.getcwd()

    mulu_name = "part0001.md"
    mulu_path = os.path.join(path, mulu_name)
    if not os.path.exists(mulu_path):
        raise ValueError("no mulu file")
    with open(mulu_path, 'r', encoding='utf-8') as f:
        content = f.read()
    reg_string1 = r"\[(.+?)\]\(.+?(part)\)"


# zhi

def lower_header_level_in_md_files(path=None):
    if path is None:
        path = os.getcwd()

    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    reg_string_head = re.compile(r"(#{1,6}) (.+)")
    # what is compile
    for file in files_md:
        try:
            with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                lines = f.readlines()

            processed_lines = []
            for line in lines:
                match = reg_string_head.search(line)
                if match:
                    string_sharp = match.group(1)
                    head_num = string_sharp.count("#")
                    line = reg_string_head.sub(
                        (head_num + 1) * "#" + r" \2", line)
                processed_lines.append(line)

            with open(os.path.join(path, file), "w", encoding="utf-8") as f:
                f.writelines(processed_lines)
        except Exception as e:
            print(f"Failed to process file {file} due to {str(e)}")


def prepend_filename_as_header_if_chapter_present(directory=None):
    reg_string1 = r"\d{3}_(第.{1,2}章.+)"
    reg_string2 = r"\d{3}_(\d{1,2} .+)\.md"

    if directory is None:
        directory = os.getcwd()
    reg_string = reg_string2
    files_md = [f for f in os.listdir(directory) if f.endswith('.md')]
    # Iterate over all files in the directory
    for filename in files_md:
        # If the filename contains 'Chapter'
        match = re.search(reg_string, filename)
        if match:
            chapter_name = match.group(1)
            print(chapter_name)
            # Open the file and read its contents
            with open(os.path.join(directory, filename), 'r', encoding="utf-8") as f:
                content = f.readlines()

            # Prepend the filename as a level 2 header
            content.insert(0, f'## {chapter_name}\n')

            # Write the modified content back to the file
            with open(os.path.join(directory, filename), 'w', encoding="utf-8") as f:
                f.writelines(content)


def remove_md_copy_code(path=None):
    if path is None:
        path = os.getcwd()
    reg_string_copy_code = [r"```\n(.+)Copy code", r"```\1\n"]
    reg_string_list = []
    reg_string_list.append(reg_string_copy_code)

    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, path, files_md)


def perform_regex_replacement_on_index_file(directory_path=None):
    """
    This function checks for the existence of an index file in the given directory
    path and performs a regex replacement on it.
    Args:
        directory_path: Path to the directory to check. Defaults to the current working directory.
    Raises:
        FileNotFoundError: If the index file is not found in the directory.
    """
    if directory_path is None:
        directory_path = os.getcwd()

    index_filename = "000_index.md"

    if index_filename not in os.listdir(directory_path):
        raise FileNotFoundError("Index file not found")

    file_paths = [os.path.join(directory_path, index_filename)]
    regex_patterns = [(r"- \[(.+)\]\(.+\)", r"\1")]

    file_operations_utils.perform_regex_replacement_on_files(
        regex_patterns, directory_path, file_paths)


def perform_regex_replacement_on_zhi_mds(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []
    reg_index_link = [
        r"-\s+\[.+\]\(https://www.zhihu.com/pub/reader/.+\)\n", r""]
    reg_string_list.extend([reg_index_link])
    reg_zhi_sao_ma = [
        r"扫码下载知乎APP 客户端\n\n!\[\]\(.+sidebar-download-qrcode.wybWudky.png\)\n", r""]
    reg_string_list.extend([reg_zhi_sao_ma])
    reg_Back_matter_template = [r"---\n\n- created:.+\n- source: .+", r""]
    reg_string_list.extend([reg_Back_matter_template])

    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def convert_zhi_footnote_to_obsidian(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []
    # r"[\[1\]](https://www.zhihu.com/pub/reader/120057501/chapter/1302455544230445056#n1s) 在英语中，发散一词是diffuse。注意focused（专注）一词的词尾是-ed，而diffuse则不是。发散一词的意思是“薄薄地弥漫出去”。"
    reg_string1 = [
        r'<sup><a href="https://www\.zhihu\.com/pub/reader.+n\d{1,2}" id="n\d{1,2}s">\[(\d{1,2})\]</a></sup>', r"[^\1]"]
    # r'<sup><a href="https://www\.zhihu\.com/pub/reader.+n\d{1,2}" id="n\d{1,2}s">\[\d{1,2}\]</a></sup>'
    reg_string_list.extend([reg_string1])
    reg_string2 = [
        r'\[\\\[(\d{1,2})\\\]\]\(https://www\.zhihu\.com/pub/.+\) (.+)', r"[^\1]: (\2)"]
    reg_string_list.extend([reg_string2])

    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def perform_regex_replacement_on_zhi_book_mds_name(path=None):
    if path is None:
        path = os.getcwd()
    files_md = [f for f in os.listdir(path) if f.endswith('.md')]
    reg_string_dir = [r"(.+) - .+ - 知乎书店", r"\1"]
    reg_string_md = [r"(.+) - .+ - 知乎书店(\.md)", r"\1\2"]
    reg_string_md2 = [r"{ (.+) }", r"{\1}"]
    reg_string_list = []
    reg_string_list.append(reg_string_md)
    file_operations_utils.perform_regex_rename_on_files(
        reg_string_list, path, files_md)
    dirs = [directory for directory in os.listdir(
        path) if os.path.isdir(directory)]
    reg_string_list = []
    reg_string_list.append(reg_string_dir)
    file_operations_utils.perform_regex_rename_on_files(
        reg_string_list, path, dirs)


def num2str_title(num):
    return str(num).zfill(3)


def rename_files_base_on_index_markdown(path=None):
    counter = 0
    if path is None:
        path = os.getcwd()
    with open(os.path.join(path, "000_index.md"), 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    files = os.listdir(path)
    for i, line in enumerate(lines):
        line = line.strip().replace("%", "_")
        note_name = line + '.md'
        if note_name in files:
            counter += 1
            os.replace(os.path.join(path, note_name),
                       os.path.join(path, num2str_title(counter) + "_" + note_name))
        else:
            print(files)
            raise FileNotFoundError(f"{note_name} not in the files list")


def get_md_files(directory='.'):
    """Return a sorted list of markdown filenames in a given directory."""
    files = [f for f in os.listdir(directory) if f.endswith('.md')]
    # Extract numeric prefix and sort based on it
    files.sort(key=lambda x: int(re.match(r'(\d{3})_', x).group(
        1)) if re.match(r'(\d{3})_', x) else float('inf'))
    return files


def check_md_files(files):

    # Check if files are in expected order
    for i, filename in enumerate(files):
        expected_prefix = f"{i:03d}_"
        if not filename.startswith(expected_prefix):
            print(
                f"Warning: {filename} does not match expected prefix {expected_prefix}")


def merge_files(filenames, output_filename):
    """Merge the content of a list of files and write to a new file."""
    with open(output_filename, 'w', encoding='utf-8') as outfile:
        for fname in filenames:
            try:
                with open(fname, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    outfile.write(content)
                    outfile.write('\n')  # add blank lines between files
            except IOError:
                print(f'Error opening file {fname}, skipping.')


def merge_all_md_files_into_one():
    """Merge all markdown files in the current directory into one file."""
    root_path, root_dir = file_operations_utils.get_assets_root_path()
    output_file = os.path.join(root_path, root_dir+".md")
    md_files = get_md_files()
    check_md_files(md_files)
    merge_files(md_files, output_file)


def Merge_all_md_files_into_one_file_base_on_num_index():
    files = [f for f in os.listdir() if f.endswith('.md')]
    files.sort()
    print(files)
    root_path, root_dir = file_operations_utils.get_assets_root_path()
    with open(os.path.join(root_path, root_dir+".md"), 'w', encoding='utf-8') as f:
        for file in files:
            with open(file, 'r', encoding='utf-8') as f2:
                content = f2.read()
                f.write(content)
                f.write('\n\n')
