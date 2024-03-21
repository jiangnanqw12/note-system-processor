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

    try:
        with open(filename, 'r') as file:
            data = json.load(file)

    except FileNotFoundError:
        data = []

    if new_record not in data:
        data.append(new_record)
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        return True
    return False


def add_id(path=None, file_type="md", areas_type="CS", name="zzz", description="This is a markdown file"):
    new_id = generate_id()
    # new_id = "0c8d77ba"
    if path is None:
        path = os.getcwd()
    id_path = os.path.join(
        global_config.KG_system_pre_file_path, global_config.IDS_path)
    if record_data(new_id, file_type, areas_type, name, description, id_path):
        print(f"New record with ID '{new_id}' has been recorded.")
    else:
        print(f"Record with ID '{new_id}' already exists.")

    return new_id


def main():
    print(add_id(path=None, file_type="md", areas_type="CS",
          name="zzz", description="This is a markdown file"))


if __name__ == "__main__":
    main()
