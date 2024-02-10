#!/usr/bin/env python
import os
import sys
import subprocess
import glob
import shutil

start_arguments = sys.argv[1:]
original_arguments = start_arguments

rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)


def check_file_type(file):
    if not "." in file:
        return False
    extension = file.split(".")[-1].lower()
    extension = extension.split("?")[0]
    if extension == "gif":
        return True
    elif extension == "png":
        return True
    elif extension == "jpg":
        return True
    elif extension == "jpeg":
        return True
    else:
        return False


def help_menu():
    script_name = os.path.basename(__file__)
    print(f'''
    [ The img Kitty extension ]
    Easier way to show (multiple) images in the Kitty terminal

    [ USAGE ]
    Show images:
      {script_name} /path/to/image.jpg
      {script_name} /path/to/image.png /path/to/other/image.jpeg
      {script_name} /path/to/images*

    Show image(s) at terminal maximum resolution:
      {script_name} -f /path/to/image.jpg
      {script_name} --full /path/to/image.jpg

    Show image(s) at maximum resolution:
      {script_name} -m /path/to/image.jpg
      {script_name} --max /path/to/image.jpg

    Show image(s) underneath text (z-index=-1):
      {script_name} -b /path/to/image.jpg
      {script_name} --behind /path/to/image.jpg
      {script_name} -m -b /path/to/image.jpg

    Clear images shown on screen:
      {script_name} -c
      {script_name} --clear

    Help Menu (this page):
      {script_name} -h
      {script_name} --help
    ''')
    exit()


kitten = shutil.which("kitten")
if kitten is None:
    print("Cannot find kitten application")
    exit(1)

show_maximum_image = False
show_terminal_max_image = False
behind_text = False
to_be_removed = []
arguments = []
temp_arguments2 = start_arguments
for argument in temp_arguments2:
    if argument[0] == "-" and "." not in argument:
        if argument.lower() == "-m" or argument.lower() == "--max":
            show_maximum_image = True
        elif argument.lower() == "-f" or argument.lower() == "--full":
            show_terminal_max_image = True
        elif argument.lower() == "-c" or argument.lower() == "--clear":
            subprocess.run([kitten, "icat", "--clear"])
            exit()
        elif argument.lower() == "-h" or argument.lower() == "--help":
            help_menu()
        elif argument.lower() == "-b" or argument.lower() == "--behind":
            behind_text = True
        else:
            print("Warning: Argument '" + argument + "' does not exist")
    else:
        arguments.append(argument)

if len(arguments) == 1:
    if os.path.isdir(arguments[0]):
        folder_path = arguments[0]
        if folder_path[-1] != "/":
            folder_path += "/"
        arguments = []
        for file in glob.glob(folder_path + "*"):
            arguments.append(file)
    elif arguments[0] == "--help" or arguments[0] == "-h":
        help_menu()
elif len(arguments) > 1:
    temp_arguments = []
    for arg in arguments:
        if os.path.isdir(arg):
            for file in glob.glob(arg + "*"):
                if check_file_type(file) == True:
                    temp_arguments.append(file)
        else:
            if check_file_type(arg) == True:
                temp_arguments.append(arg)
    arguments = temp_arguments

something_showed_up = False
first_one_shown = False

if len(arguments) > 1:
    current_top = 0
    current_left = 0
    reached_bottom = False
    for arg in arguments:
        if not check_file_type(arg):
            continue
        something_showed_up = True
        if show_maximum_image:
            if behind_text:
                subprocess.run([kitten, "icat", "-z=-1", arg])
            else:
                subprocess.run([kitten, "icat", arg])
        elif show_terminal_max_image:
            if behind_text:
                if not first_one_shown:
                    subprocess.run([kitten, "icat", "-z=-1",
                                    "--place=" + str(columns) + "x" + str(rows - 1) + "@" + "0x0", "--align", "center",
                                    arg])
                    first_one_shown = True
                else:
                    print()
                    subprocess.run([kitten, "icat", "-z=-1",
                                    "--place=" + str(columns) + "x" + str(rows) + "@" + "0x" + str(rows), "--align",
                                    "center", arg])
            else:
                if not first_one_shown:
                    subprocess.run(
                        [kitten, "icat", "--place=" + str(columns) + "x" + str(rows - 1) + "@" + "0x0",
                         "--align", "center", arg])
                    first_one_shown = True
                else:
                    print()
                    subprocess.run([kitten, "icat",
                                    "--place=" + str(columns) + "x" + str(rows) + "@" + "0x" + str(rows), "--align",
                                    "center", arg])
        else:
            if behind_text:
                subprocess.run([kitten, "icat", "-z=-1",
                                "--place=" + str(columns // 4) + "x19" + "@" + str(current_left) + "x" + str(current_top),
                                "--align", "left", arg])
            else:
                subprocess.run([kitten, "icat",
                                "--place=" + str(columns // 4) + "x19" + "@" + str(current_left) + "x" + str(current_top),
                                "--align", "left", arg])
            if arg == arguments[-1]:
                if reached_bottom:
                    print("\n")
                exit()
            current_left += (columns // 4)
            if reached_bottom:
                if current_left > columns - 6:
                    current_left = 0
                    for i in range(19):
                        print()
            elif current_left > columns - 6:
                current_left = 0
                current_top += 19
                if current_top > rows - 10:
                    reached_bottom = True
                    current_top = rows - 19
                    for i in range(19):
                        print()

elif len(arguments) == 1:
    if check_file_type(arguments[0]):
        something_showed_up = True
        if show_maximum_image:
            if behind_text:
                subprocess.run([kitten, "icat", "-z=-1", arguments[0]])
            else:
                subprocess.run([kitten, "icat", arguments[0]])
        elif show_terminal_max_image:
            if behind_text:
                subprocess.run(
                    [kitten, "icat", "-z=-1", "--place=" + str(columns) + "x" + str(rows - 1) + "@" + "0x0",
                     "--align", "center", arguments[0]])
            else:
                subprocess.run(
                    [kitten, "icat", "--place=" + str(columns) + "x" + str(rows - 1) + "@" + "0x0",
                     "--align", "center", arguments[0]])
        else:
            if behind_text:
                subprocess.run([kitten, "icat", "-z=-1", "--place=" + str(columns // 4) + "x20" + "@" + str(
                    columns - (columns // 4)) + "x" + str(rows - 21), "--align", "left", arguments[0]])
            else:
                subprocess.run([kitten, "icat", "--place=" + str(columns // 4) + "x20" + "@" + str(
                    columns - (columns // 4)) + "x" + str(rows - 21), "--align", "left", arguments[0]])
elif len(original_arguments) == 0:
    help_menu()

if not something_showed_up:
    print("No images found")
