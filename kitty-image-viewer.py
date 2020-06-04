#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import glob


startarguments = sys.argv[1:]
originalarguments = startarguments

rows, columns = os.popen('stty size', 'r').read().split()
rows = int(rows)
columns = int(columns)

def checkFileType(file):
	if not "." in file:
		return False
	extension = file.split(".")[-1].lower()
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

def helpmenu():
	print (
		"[ The img Kitty extension ]\n"+
		" Easier way to show (multiple) images in the Kitty terminal\n\n"+
		"[ USAGE ]\n"+
		" Show images:\n"+
		"   img /path/to/image.jpg\n"+
		"   img /path/to/image.png /path/to/other/image.jpeg\n"+
		"   img /path/to/images*\n"+
		" Show image(s) at terminal maximum resolution:\n"+
		"   img -f /path/to/image.jpg\n"+
		"   img --full /path/to/image.jpg\n"+
		" Show image(s) at maximum resolution:\n"+
		"   img -m /path/to/image.jpg\n"+
		"   img --max /path/to/image.jpg\n"+
		" Show image(s) underneeth text (z-index=-1)\n"+
		"   img -b /path/to/image.jpg\n"+
		"   img --behind /path/to/image.jpg\n"+
		"   img -m -b /path/to/image.jpg\n"+
		" Clear images shown on screen:\n"+
		"   img -c\n"+
		"   img --clear\n"+
		" Help Menu (this page):\n"+
		"   img -h\n"+
		"   img --help"
	)
	exit()


showMaximumImage = False
showTerminalMaxImage = False
behindText = False
toBeRemoved = []
arguments = []
temparguments2 = startarguments
for argument in temparguments2:
	if argument[0] == "-" and "." not in argument:
		if argument.lower() == "-m" or argument.lower() == "--max":
			showMaximumImage = True
		elif argument.lower() == "-f" or argument.lower() == "--full":
			showTerminalMaxImage = True
		elif argument.lower() == "-c" or argument.lower() == "--clear":
			subprocess.run(["/usr/bin/kitty", "icat", "--clear"])
			exit()
		elif argument.lower() == "-h" or argument.lower() == "--help":
			helpmenu()
		elif argument.lower() == "-b" or argument.lower() == "--behind":
			behindText = True
		else:
			print ("Warning: Argument '"+argument+"' does not exist")
	else:
		arguments.append(argument)


if len(arguments) == 1:
	if os.path.isdir(arguments[0]):
		folderpath = arguments[0]
		if folderpath[-1] != "/":
			folderpath += "/"
		arguments = []
		for file in glob.glob(folderpath + "*"):
			arguments.append(file)
	elif arguments[0] == "--help" or arguments[0] == "-h":
		helpmenu()
elif len(arguments) > 1:
	temparguments = []
	for arg in arguments:
		if os.path.isdir(arg):
			for file in glob.glob(arg + "*"):
				if checkFileType(file) == True:
					temparguments.append(file)
		else:
			if checkFileType(arg) == True:
				temparguments.append(arg)
	arguments = temparguments


somethingshowedup = False
firstOneShown = False

if len(arguments) > 1:
	currenttop = 0
	currentleft = 0
	reachedbottom = False
	for arg in arguments:
		if checkFileType(arg) == False:
			continue
		somethingshowedup = True
		if showMaximumImage == True:
			if behindText == True:
				subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", arg])
			else:
				subprocess.run(["/usr/bin/kitty", "icat", arg])
		elif showTerminalMaxImage == True:
			if behindText == True:
				if firstOneShown == False:
					subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", "--place=" + str(columns)+"x"+str(rows-1)+"@"+"0x0", "--align", "center", arg])
					firstOneShown = True
				else:
					print()
					subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", "--place=" + str(columns)+"x"+str(rows)+"@"+"0x"+str(rows), "--align", "center", arg])
			else:
				if firstOneShown == False:
					subprocess.run(["/usr/bin/kitty", "icat", "--place=" + str(columns)+"x"+str(rows-1)+"@"+"0x0", "--align", "center", arg])
					firstOneShown = True
				else:
					print()
					subprocess.run(["/usr/bin/kitty", "icat", "--place=" + str(columns)+"x"+str(rows)+"@"+"0x"+str(rows), "--align", "center", arg])
		else:
			if behindText == True:
				subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", "--place=" + str(columns//4)+"x19"+"@"+str(currentleft)+"x"+str(currenttop), "--align", "left", arg])
			else:
				subprocess.run(["/usr/bin/kitty", "icat", "--place=" + str(columns//4)+"x19"+"@"+str(currentleft)+"x"+str(currenttop), "--align", "left", arg])
			if arg == arguments[-1]:
				if reachedbottom == True:
					print ("\n")
				exit()
			currentleft+=(columns//4)
			if reachedbottom == True:
				if currentleft > columns-6:
					currentleft = 0
					for i in range(19):
						print ()
			elif currentleft > columns-6:
				currentleft = 0
				currenttop+=19
				if currenttop > rows-10:
					reachedbottom = True
					currenttop = rows-19
					for i in range(19):
						print ()
			
elif len(arguments) == 1:
	if checkFileType(arguments[0]) == True:
		somethingshowedup = True
		if showMaximumImage == True:
			if behindText == True:
				subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", arguments[0]])
			else:
				subprocess.run(["/usr/bin/kitty", "icat", arguments[0]])
		elif showTerminalMaxImage == True:
			if behindText == True:
				subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", "--place=" + str(columns)+"x"+str(rows-1)+"@"+"0x0", "--align", "center", arguments[0]])
			else:
				subprocess.run(["/usr/bin/kitty", "icat", "--place=" + str(columns)+"x"+str(rows-1)+"@"+"0x0", "--align", "center", arguments[0]])
		else:
			if behindText == True:
				subprocess.run(["/usr/bin/kitty", "icat", "-z=-1", "--place=" + str(columns//4)+"x20"+"@"+str(columns-(columns//4))+"x"+str(rows-21), "--align", "left", arguments[0]])
			else:
				subprocess.run(["/usr/bin/kitty", "icat", "--place=" + str(columns//4)+"x20"+"@"+str(columns-(columns//4))+"x"+str(rows-21), "--align", "left", arguments[0]])
elif len(originalarguments) == 0:
	helpmenu()

if somethingshowedup == False:
	print ("No images found")