import os
import file_operations_utils


def remove_wiki_edit_link(directory_path=None):

    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_wiki_edit_link = [
        r'\\\[\[edit\]\(https://en\.wikipedia\.org/w/index\.php\?title=.+ "Edit section: (.+)"\)\\\]', r""]
    reg_string_list.extend([reg_wiki_edit_link])

    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)


def remove_wiki_equation_svg(directory_path=None):
    if directory_path is None:
        directory_path = os.getcwd()

    files_md = [f for f in os.listdir(directory_path) if f.endswith('.md')]

    reg_string_list = []

    reg_wiki_equation_svg = [r'!\[([^\]]+)\]\([A-Za-z0-9]+\.svg\)', r"$\1$"]

    reg_string_list.extend([reg_wiki_equation_svg])

    file_operations_utils.perform_regex_replacement_on_files(
        reg_string_list, directory_path, files_md)
