#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Let viewers pay currency to boost currency payouts
for everyone in chat for x seconds"""
import json
import os, os.path
import operator
import time
import codecs
import glob

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "CheckOptions"
Website = "https://www.twitch.tv/newtc"
Creator = "Newt"
Version = "1.0.0.0"
Description = "Displays all options users can add currency to for voting"

#---------------------------------------
# Versions
#---------------------------------------
"""
1.0.0.0 - Initial release
"""
#---------------------------------------
# Variables
#---------------------------------------
settingsFile = os.path.join(os.path.dirname(__file__), "settings.json")

#---------------------------------------
# Classes
#---------------------------------------
class Settings:
    """
    Tries to load settings from file if given
    The 'default' variable names need to match UI_Config"""
    def __init__(self, settingsFile=None):
        if settingsFile is not None and os.path.isfile(settingsFile):
            with codecs.open(settingsFile, encoding='utf-8-sig', mode='r') as f:
                self.__dict__ = json.load(f, encoding='utf-8-sig')

        else: #set variables if no settings file
            self.Enabled = True
            self.OnlyLive = False
            self.Command = "!checkOptions"
            self.Cost = 0
            self.UseCD = False
            self.Cooldown = 5
            self.cd_response = "{0} the command is still on cooldown for {1} seconds!"
    def ReloadSettings(self, data):
        """Reload settings on save through UI"""
        self.__dict__ = json.loads(data, encoding='utf-8-sig')
        return


    def SaveSettings(self, settingsFile):
        """Save settings to files (json and js)"""
        with codecs.open(settingsFile, encoding='utf-8-sig', mode='w+') as f:
            json.dump(self.__dict__, f, encoding='utf-8-sig')
        with codecs.open(settingsFile.replace("json", "js"), encoding='utf-8-sig', mode='w+') as f:
            f.write("var settings = {0};".format(json.dumps(self.__dict__, encoding='utf-8-sig')))
        return

def ReloadSettings(jsonData):
    """Reload settings"""
	# Globals
    global MySet

	# Reload saved settings
    MySet.ReloadSettings(jsonData)

	# End of ReloadSettings
    return

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Required tick function"""
    # Globals
    global MySet
    global m_Active
    m_Active = False
    # Load in saved settings
    MySet = Settings(settingsFile)

    # End of Init
    return

def Execute(data):
	"""Required Execute function"""
	currentMax = 0
	changedName = 'missingFile'
	retVal = ''
	files = dict()

	if data.IsChatMessage() and data.GetParam(0).lower() == MySet.Command.lower():
		
		for filename in glob.glob('Services/Twitch/Votes/*.txt'):
			#Load in all the file information we need
			f = codecs.open(filename, 'r', encoding='utf-8-sig')
			fileValue = int(f.read())
			
			changedName = filename
			changedName = changedName.split('\\', 1)[-1]
			changedName = changedName.split('.')[0]
			files[changedName] = fileValue
        
		#sort by the keys https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value
		sortedFiles = sorted(files.items(), key=operator.itemgetter(1))
		
		#add all sorted values to retval and return.
		for x, y in reversed(sortedFiles):
			retVal += str(x)
			
			#if the value is higher than 0, add the value
			if (files[x] > 0):
				retVal += '('+str(y)+' logs)'
			
			retVal += ', '
		
        retVal = retVal[:-2]
        
		#sends the final message
        respond(data, retVal)
        
	return

def Tick():
    """Required tick function"""
    return

def respond(data, output):
    retVal = output
    
    # If the original message is from a discord message
    if data.IsFromDiscord():
        # if the original message is from a whisper
        if data.IsWhisper():
            Parent.SendDiscordDM(data.User, retVal)
        else:
            Parent.SendDiscordMessage(retVal)
    # If the original message is from a live stream
    else:
        if data.IsWhisper():
            Parent.SendStreamWhisper(data.UserName, retVal)
        else:
            Parent.SendStreamMessage(str(retVal))