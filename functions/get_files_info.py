import os
from functions.config import MAX_CHARS

def get_files_info(working_directory, directory=None):
    try:

        abs_work_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(abs_work_dir, directory))

        if not full_path.startswith(abs_work_dir):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'


        files = []
        for file in os.listdir(full_path):
            file_dir = os.path.join(full_path, file)
            files.append(f"- {file} file_size={os.path.getsize(file_dir)}, is_dir={os.path.isdir(file_dir)}")
        return "\n".join(files)
    except Exception as e:
        return f"Error: {str(e)}"
    
def get_file_content(working_directory, file_path):
        abs_work_dir = os.path.abspath(working_directory)
        full_path = os.path.abspath(os.path.join(abs_work_dir, file_path))

        if not full_path.startswith(abs_work_dir):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        try:
            with open(full_path, "r") as f:
                file_content_string = f.read(MAX_CHARS)
                if len(file_content_string) > MAX_CHARS:
                    file_content_string = file_content_string[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                return file_content_string
        except FileNotFoundError:
            return f'Error: File not found or is not a regular file: "{file_path}"'