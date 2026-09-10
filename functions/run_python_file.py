import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))
        if os.path.commonpath([abs_working_dir, absolute_file_path]) != abs_working_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", absolute_file_path]
        # print(command)
        if args != None:
            command.extend(args)
        # print(command)
        obj = subprocess.run(command, cwd=abs_working_dir, capture_output=True, timeout=30, text=True)
        output_string = ""
        if obj.returncode != 0:
            output_string += f"<Process exited with code {obj.returncode}>\n"
        if obj.stdout == "" and obj.stderr == "":
            output_string += "<No output produced>\n"
        else:
            if obj.stdout != "":
                output_string += f"<STDOUT: {obj.stdout}>\n"
            if obj.stderr != "":
                output_string += f"<STDERR: {obj.stderr}>\n"     
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes/runs and returns the output of a specified python file, constrained to the working directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The path to the python file to run, relative to the working directory."
                },
                "args":{
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional arguments to pass to the Python script."
                }
            },
            "required": ["file_path"]
        }
    }
}