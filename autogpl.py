#!/bin/python
# -*- coding: utf-8 -*-

# /\ # Hellooooo again ! 30 may 2013
# \/ # This script is still under GPL license
# /\ # But i still don't care about legal header toussatoussa...
# \/ # So.. Copyright (C)myself (aka: aquila) 2013-3013 again

import os
import sys
import shutil

def manHelpToussa():
	"""
	Case of wrong use
	"""
	print("Read the sources for details")
	print('Example : autogpl.py sourcedir --owner "machin machin" --project "superproject" ')
	print("Don't forget the quotes !!")
	
def gplheader(owner, project):
	header = """// Copyright (C) 2013 """ + owner + """
//
// This file is part of """ + project + """.
// 
// """ + project + """ is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// """ + project + """ is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with """ + project + """.  If not, see <http://www.gnu.org/licenses/>.
	\n"""
	return header
	
def autogpl(directory, owner, project):
	"""
	Add GPL header to all c/c++ files in directory
	Output: copy of directory with _gpl suffix
	"""
	fileList = list()
	if(directory[-1:]=='/'):
		directory = directory[:-1]
	output = directory + "_gpl"
	print(output)
	if(os.path.exists(output)):
		print("Directory already exists")
		return
	
	shutil.copytree(directory, output)
	for path, dirs, files in os.walk(output):
		for f in files:
			fileName, ext = os.path.splitext(f)
			if ext ==".h" or ext == ".c" or ext == ".cpp" or ext == ".hpp":
				fileList.append(path + "/" + f)
	for elt in fileList:
		with open(elt, 'r') as myfile:
			readFile= gplheader(owner, project) + myfile.read()
		with open(elt, 'w') as gplFile:
			gplFile.write(readFile)

### Executed as standalone:
if __name__ == '__main__' :
	arglen = len(sys.argv)
	if arglen != 6:
		manHelpToussa()
	elif sys.argv[2] == str("--owner") and sys.argv[4] == str("--project"):
		autogpl(sys.argv[1], sys.argv[3], sys.argv[5])