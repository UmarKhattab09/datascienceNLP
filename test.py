import os
import pathlib
import sys

folder_path = pathlib.Path(__file__).parent.resolve()
parent_path = os.path.join(folder_path, '.')
sys.path.append(parent_path)

print("Current script folder:", folder_path)
print("Appended parent path:", parent_path)
