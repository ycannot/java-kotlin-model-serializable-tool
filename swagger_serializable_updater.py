# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:12:05 2020

@author: yigit
"""

import datetime
import glob
import os


def clear():
    # for windows

    if os.name == 'nt':
        os.system('cls')

        # for mac and linux(here, os.name is 'posix') 
    else:
        os.system('clear')


clear()
path = r"C:\Users\yigit\Desktop\client"
inp = str(input("Please enter a filepath of src\main\java\io\swagger\client: "))
path = inp
list_subfolders_with_paths = [f.path for f in os.scandir(path) if f.is_dir()]

if list_subfolders_with_paths == []:
    list_subfolders_with_paths == [path]

text = "Please select a subdirectory to implement serializable"
for i in range(len(list_subfolders_with_paths)):
    text += "\n" + str(i) + ". " + list_subfolders_with_paths[i][len(path)::]
selected = -1
while (not 0 <= selected < len(list_subfolders_with_paths)):
    clear()
    print(text)
    selected = int(input("Please select: "))
    print()

os.chdir(list_subfolders_with_paths[selected])
for file in glob.glob("*.java"):
    print(file)

input("\n" + str(len(glob.glob("*.java"))) + " file(s) will be affected in " + list_subfolders_with_paths[
    selected] + ". Do you want to update these files?\n\nPress any keys to continue or Ctrl+C to exit")

unchanged = "\n\nFile(s) Unchanged:"
changed = "File(s) Changed:"
log = open("swagger_update_log.log", "a", encoding="UTF-8")
for file in glob.glob("*.java"):
    input_file = open(file, "r", encoding="UTF-8")
    temp = input_file.read()
    input_file.close()

    input_file = open(file, "w", encoding="UTF-8")

    if temp.count("public class") > 0:
        start_index = temp.find("public class") + 12
        end_index = temp.find("{")
        if (temp[start_index:end_index].count("Serializable") > 0):
            unchanged += "\n" + file
        else:
            if temp.count("import java.io.Serializable") == 0:
                import_index = temp.find("import")
                temp = temp[0:import_index] + "import java.io.Serializable;\n" + temp[import_index::]
                start_index = temp.find("public class") + 12
                end_index = temp.find("{")

            if not temp[start_index:end_index].count("implements") > 0:
                temp = temp[0:end_index] + "implements Serializable " + temp[end_index::]
            else:
                end_index = temp.find("implements") + 10
                temp = temp[0:end_index] + " Serializable," + temp[end_index::]
            changed += "\n" + file
    else:
        unchanged += "\n" + file

    input_file.write(temp)
    input_file.close()

log.write("\n\n------------------------------------\n" + str(
    datetime.datetime.now()) + "\n------------------------------------\n" + changed + unchanged)
log.close()
