import os


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