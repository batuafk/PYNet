import shutil
import os

file_name = "Client"
icon = "exe.ico"

with open(f"{file_name}.py", "r") as file:
    code = file.read()

os.system(f"pyinstaller --noconsole --onefile --icon={icon} {file_name}.py")
shutil.rmtree("build")
os.remove(f"{file_name}.spec")

os.system("pause")
