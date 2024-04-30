import uuid
import json
import os
import global_config


def generate_id():
    return str(uuid.uuid4())[:8]


def record_data(new_id, file_type="md", areas_type="CS", name="zzz", description="This is a markdown file", filename='data.json'):
    new_record = {
        'id': new_id,
        'file_type': file_type,
        'areas_type': areas_type,
        'name': name,
        'description': description
    }
    data = []
    try:
        with open(filename, 'r', encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        pass

    if new_record not in data:
        data.append(new_record)
        with open(filename, 'w', encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
        return True
    return False


def add_default_id(path=None, file_type="zzz", areas_type="zzz", name="zzz", description="This is a zzz file", TR_MODE=False):
    new_id = generate_id()
    # new_id = "0c8d77ba"
    if path is None:
        path = os.getcwd()
    id_path = os.path.join(
        global_config.KG_system_pre_file_path, global_config.IDS_path)
    if record_data(new_id, file_type, areas_type, name, description, id_path):
        if TR_MODE:
            print(f"New record with ID '{new_id}' has been recorded.")
    else:
        print(f"Record with ID '{new_id}' already exists.")
        raise Exception("Record with ID already exists")

    return new_id


def rename_files_with_id():
    TR_MODE = True
    path = os.getcwd()
    # all the mp3 files in the current directory
    files_mp3 = [f for f in os.listdir(path) if f.endswith('.mp3')]
    for file in files_mp3:
        id = add_default_id(path, "mp3", "English",
                            file, "This is a audio file", TR_MODE=TR_MODE)
        if TR_MODE:
            print(f"File '{file}' has been assigned ID '{id}'.")
        new_name = f"{file[:-4]}_{id}.mp3"
        os.rename(file, new_name)


def main():
    print(add_default_id(path=None, file_type="zzz", areas_type="zzz",
          name="zzz", description="This is a markdown file"))


if __name__ == "__main__":
    main()
