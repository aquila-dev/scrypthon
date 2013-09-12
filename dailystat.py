#!/usr/bin/python3
# -*- coding: utf-8 -*- 
'''
@author Manu / Njibhu@quakenet / ghost-404@skype / <em.viala@gmail.com>
@brief Get the stat from dailymotion and append it to a file with details...
'''

import re
import urllib.request
import datetime
import json

#Passer le single digit en dual
def formatDate(dateToFormat):
	'''Take an integer, if it's a single digit, it return a version with 0 on top of it'''
	if len(str(dateToFormat)) == 1:
		day = "0" + str(dateToFormat)
	else:
		day = str(dateToFormat)
	return day

def getStreamName(now):
	'''Get the actual stream title, its arg is a datetime'''
	eclypsiaChannel = "http://www.eclypsia.com/fr/ZeratoR"
	
	actualDay = formatDate(now.day) + "/" + formatDate(now.month)
	
	#Récup de la page elcypsia
	page = str(urllib.request.urlopen(eclypsiaChannel).read())
	pyFind2 = re.compile(actualDay)
	finding = re.finditer(pyFind2, page)
	dailyProgram = dict()
	
	#Extraction du programme du jour:
	for elt in finding:
		spanBegin,spanEnd = elt.span()
		pyFind2 = re.compile('\d{2}\:\d{2}( \- )\d{2}\:\d{2}')
		pyFind3 = re.compile('(bebas).*(</h3>)')
		findArea = page[spanEnd:spanEnd+1700]
		streamer = re.search(pyFind3, findArea).group()
		pyFind3 = re.compile('(>).*(<)')
		streamer = re.search(pyFind3, streamer).group()
		dailyProgram[re.search(pyFind2, findArea).group()] = streamer[1:len(streamer)-1]
	
	#Recherche du programme actuel:
	for elt in dailyProgram:
		beginningProgram = elt[0:5]
		beginningProgram = beginningProgram.split(':')
		beginningProgram = datetime.time(int(beginningProgram[0]),int(beginningProgram[1]))
		endingProgram = elt[8:]
		endingProgram = endingProgram.split(':')
		endingProgram = datetime.time(int(endingProgram[0]),int(endingProgram[1]))
		if now.time() > beginningProgram and now.time() < endingProgram:
			return dailyProgram[elt]	
		
	return str("Hors-programme")

			
def main():
	'''Get the current number of viewers, the stream title, and parse it with json'''
	#Chaine de ZeratoR:
	liveChaine = "xsv561"
	destinationFile = "/home/njibhu/"
	
	#Récupération de l'audience
	audience = str(urllib.request.urlopen("https://api.dailymotion.com/video/" + liveChaine + "?fields=audience").read())
	pyFind = re.compile("\{(.*)\}")
	audience = re.search(pyFind, audience).group()
	audience = json.loads(audience)
	now = datetime.datetime.now()
	
	#Ajout des champs de date/time ainsi que du stream actuel en json
	audience['day'] = now.day
	audience['month'] = now.month
	audience['hour'] = now.hour
	audience['minute'] = now.minute
	audience['streamer'] = getStreamName(now)
	
	if str(audience['audience']).isdigit() == False:
		audience['audience'] = 0
		
	#Dump du json et ajout a la fin du fichier de stat portant le nom du jour
	filename = destinationFile + str(now.day) + "-" + str(now.month) + "-" + str(now.year) + ".txt"
	with open(filename, "a") as statFile:
		statFile.write(json.dumps(audience))
		statFile.write("\n")

#Use it with a cron !		
main()