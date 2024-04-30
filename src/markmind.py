import os
import logging
import file_operations_utils
import time
import urllib.parse
import re
# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Constants
TR_MODE = True
ASSETS_FOLDER_NAME = "assets"


def get_annotator_id(file_name):
    file_name_temp = file_name.replace(" ", "_")
    return file_name_temp + "_" + str(file_operations_utils.get_current_timestamp()), file_name_temp


def get_annotate_image_target_path(path):
    try:
        return path.split("KG\\")[1]
    except IndexError:
        logging.error("Invalid path format")
        return None


def create_annotator(path=None):
    if path is None:
        path = os.getcwd()
    files_annotator = [f for f in os.listdir(
        path) if f.endswith('_annotator.md')]
    # get bassets folder path
    big_assets_path = file_operations_utils.get_b_KG_directory_path(path)

    if big_assets_path is None:
        raise FileNotFoundError(
            "Could not find assets folder in current folder path")

    if TR_MODE:
        logging.debug("big_assets_path: %s", big_assets_path)

    for root, dirs, files in os.walk(big_assets_path):
        for file in files:
            if file.endswith(".pdf"):
                file_name = os.path.splitext(file)[0]
                annotator_id, file_name_temp = get_annotator_id(file_name)

                if TR_MODE:
                    logging.debug("annotator_id: %s", annotator_id)

                annotate_target_path = os.path.join(root, file)
                # annotate_target_path = urllib.parse.quote(
                #     os.path.abspath(annotate_target_path))

                annotate_image_target_full_path = os.path.join(path, "imgs")
                annotate_image_target_path = get_annotate_image_target_path(
                    annotate_image_target_full_path)

                content_annotator = f"""
---
id: {annotator_id}
annotate-type: pdf
annotate-target: file://{annotate_target_path}
annotate-image-target: {annotate_image_target_path}

---

"""

                annotator_file_name = f"{annotator_id}_annotator.md"
                annotator_path = os.path.join(path, annotator_file_name)
                reg_anno = file_name_temp+"_"+r"\d{10}"+"_annotator.md"
                flag = False
                for file_annotator in files_annotator:
                    match = re.search(reg_anno, file_annotator)
                    if match:
                        flag = True
                if not flag:
                    with open(annotator_path, "w", encoding="utf-8") as f:
                        f.write(content_annotator)


# def create_annotator(path=None):
#     if path is None:
#         path = os.getcwd()
#     TR_MODE = 1
#     # IS "\OneDrive\KG\" contained by current folder path? if not, raise error

#     # get bassets folder path
#     big_assets_path = file_operations_utils.get_b_KG_directory_path(path)
#     if TR_MODE:
#         print("big_assets_path:", big_assets_path)
#     if big_assets_path is None:
#         raise Exception("Could not find assets folder in current folder path")
#     for root, dirs, files in os.walk(big_assets_path):
#         for file in files:
#             if file.endswith(".pdf"):
#                 file_name = file.split(".")[0]
#                 file_name_temp = file_name.replace(" ", "_")
#                 annotator_id = file_name_temp+"_"+str(file_operations_utils.get_current_timestamp())
#                 if TR_MODE:
#                     print("annotator_id:", annotator_id)
#                 annotate_target_path = os.path.join(root, file)
#                 if TR_MODE:
#                     print("annotate_target_path:", annotate_target_path)
#                 annotate_image_target_full_path = os.path.join(path, "imgs")
#                 if TR_MODE:
#                     print("annotate_image_target_full_path:",
#                           annotate_image_target_full_path)
#                 # annotate_image_target_path= annotate_image_target_full_path after \OneDrive\KG\
#                 annotate_image_target_path = annotate_image_target_full_path.split(
#                     "KG\\")[1]
#                 if TR_MODE:
#                     print("annotate_image_target_path:",
#                           annotate_image_target_path)

#                 content_annotator = f"""

# ---
# id: {annotator_id}
# annotate-type: pdf
# annotate-target: file://{annotate_target_path}
# annotate-image-target: {annotate_image_target_path}
# ---

# """
#                 annotator_file_name = annotator_id + "_annotator"+".md"
#                 annotator_path = os.path.join(path, annotator_file_name)
#                 with open(annotator_path, "w", encoding="utf-8") as f:
#                     f.write(content_annotator)
