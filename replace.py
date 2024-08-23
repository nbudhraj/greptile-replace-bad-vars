import os
import re

def apply_replacements():
    replacements = [
        ["x", "numIterations", "main.py"],
        ["y", "result", "main.py"],
        ["z", "tempValue", "main.py"],
        ["a", "inputString", "utils.py"],
        ["b", "processedString", "utils.py"],
        ["c", "count", "utils.py"],
        ["d", "data", "data_processing.py"],
        ["e", "errorMessage", "error_handling.py"],
        ["f", "fileHandle", "file_operations.py"],
        ["g", "groupedData", "data_analysis.py"],
    ]
    for old_var, new_var, filename in replacements:
        if not os.path.isfile(filename):
            print(f"File {filename} does not exist.")
            continue

        with open(filename, 'r') as file:
            content = file.read()

        # Use regex to replace only whole words
        new_content = re.sub(rf'\b{re.escape(old_var)}\b', new_var, content)

        if content != new_content:  # Only write if there are changes
            with open(filename, 'w') as file:
                file.write(new_content)
            print(f"Replaced '{old_var}' with '{new_var}' in {filename}.")
        else:
            print(f"No replacements needed for {filename}.")

if __name__ == '__main__':
    apply_replacements()
