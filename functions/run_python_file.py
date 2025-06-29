import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_work_dir = os.path.abspath(working_directory)
    full_path = os.path.join(abs_work_dir, file_path)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_work_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(full_path):
        return f'Error: File "{file_path}" not found.'
    if not file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    try:
        running =  subprocess.run(['python3', full_path], timeout=30, capture_output=True, text=True)
        output = f'STDOUT: {running.stdout}\nSTDERR: {running.stderr}'
        if running.returncode != 0:
            output += f'\nProcess exited with code {running.returncode}'
        if running.stdout == "" and running.stderr == "":
            return "No output produced."
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    if running.stdout == "" and running.stderr == "":
        return "No output produced."