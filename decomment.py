#!/bin/python
# -*- coding: utf-8 -*-

# /\ # Hellooooo ! 29 may 2013
# \/ # This script is under GPL license
# /\ # But i don't care about legal header toussatoussa...
# \/ # So.. Copyright (C)myself (aka: aquila) 2013-3013
# /\ # And if someone wanna sell my work, he's a stupid useless snail <3
# \/ # because this is a pretty simple script, a nice work to up ur skills

### Read descriptions of workOnComment() and decomment() if u wanna use it
### as a module but remember, it works only with c like comments

import os
import sys
import shutil

def manHelpToussa():
	"""
	Case of wrong use, and "mode" example
	"""
	print("Read the sources for details")
	print("Example for a file: decomment -f sourcefile")
	print("Example for a directory: decomment -r sourcedir")
  
def workOnComment(source):
	"""
	source is str()
	Return a copy without comments
	"""
	state = "normal"
	commentType=""
	
	copy = str()
	for char in source:
		###STATE NORMAL
		if state == "normal":
			if char == "'":
				state = "char_litteral"
				copy += char

			elif char == '"':
				state = "string_litteral"
				copy += char

			elif char == "/":
				state = "comment_init"

			else:
				copy += char

		###STATE COMMENT_INIT
		elif state == "comment_init":
			if char == "/":
				state = "comment"
				commentType = "//"
			elif char == "*":
				state = "comment"
				commentType = "/*"
			else:
				char += "/" + char
				state = "normal"
		
		#STATE COMMENT
		elif state == "comment":
			if char == '\n' and commentType == "//":
				state = "normal"
				
			elif char == "*" and commentType == "/*":
				state = "comment_*/"
			
		#STATE COMMMENT END
		elif state == "comment_*/":
			if char == "/":
				state = "normal"
			else:
				state = "comment"
		
		#STATE STR
		elif state == "string_litteral":
			if char == '"':
				state = "normal"
			copy += char
			
		elif state == "char_litteral":
			if char == "'":
				state = "normal"
			copy += char
		
		#STATE useless
		else:
			#Troll of the day
			print("FML")
			break

	return copy

def decomment(mode, source):
	"""
	Delete C/C++ comments from source file or directory depending on mode
	Mode examples: str("-f") for a file, str("-r") for a directory
	source is a pathfile, mode: look at manHelpToussa
	No return, output is a copy with "_uncomment" suffix
	If u need returns, use the workOnComment function
	
	blblblbl have a nice day
	"""
	
	#MODE SINGLE FILE
	if mode == "-f":
		with open(source, 'r') as myfile:
			readFile = myfile.read()
		with open(source + "_uncomment", 'w') as uncommentedFile:
			uncommentedFile.write(workOnComment(readFile))
		
	#MODE RECURSIVE
	elif mode == "-r":
		fileList = list()
		outpath = source + "_uncomment"
		if(os.path.exists(outpath)):
			print("Directory already exists")
			return
			
		shutil.copytree(source, outpath)
		for path, dirs, files in os.walk(outpath):
			for f in files:
				fileName, ext = os.path.splitext(f)
				if ext ==".h" or ext == ".c" or ext == ".cpp" or ext == ".hpp":
					fileList.append(path + "/" + f)
		for elt in fileList:
			with open(elt, 'r') as myfile:
				readFile= myfile.read()
			with open(elt, 'w') as uncommentedFile:
				uncommentedFile.write(workOnComment(readFile))
	else:
		manHelpToussa()

  
### Executed as standalone:
if __name__ == '__main__' :
	arglen = len(sys.argv)
	if arglen != 3:
		manHelpToussa()
	else:
		decomment(sys.argv[1], sys.argv[2])
		