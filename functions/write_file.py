import os

def write_file(working_directory, file_path, content):
    abs_work_dir = os.path.abspath(working_directory)
    full_path = os.path.join(abs_work_dir, os.path.dirname(file_path))
    abs_file_path = os.path.join(abs_work_dir, file_path)

    if not full_path.startswith(abs_work_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Created Directory: {full_path}")
    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{full_path}" ({len(content)} characters written)'
        
    except FileNotFoundError:
        return f'Error: Error writing to {full_path}'