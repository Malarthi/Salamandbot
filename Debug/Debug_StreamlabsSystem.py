#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name
"""Allows users to engage in realtime debugging."""
import bot_globals

#---------------------------------------
# [Required] Script information
#---------------------------------------
ScriptName = "Debug"
Website = "https://www.twitch.tv/newtc"
Creator = "Malarthi"
Version = "1.0.0.0"
Description = "Allows users to engage in realtime debugging."

#---------------------------------------
# Versions
#---------------------------------------
"""
1.0.0.0 - Initial release
"""

#---------------------------------------
# [Required] functions
#---------------------------------------
def Init():
    """Required tick function"""
    # End of Init
    return

def Execute(data):
    """Required Execute function"""

    if data.IsChatMessage():
        if data.GetParamCount() == 2 and data.GetParam(0).lower() == 'debug':
            if   data.GetParam(1).lower() == 'help':
                respond("The following are valid options: " + bot_globals.__dict__.keys().copy().append(['help']))
            elif data.GetParam(1).lower() == 'all':
                respond("Dumping all available bot global values: " + bot_globals.__dict__)
            elif data.GetParam(1).lower() in bot_globals.__dict__.keys():
                respond(data.GetParam(1).lower() + ": " + bot_globals.__dict__[data.GetParam(1).lower()])

    return

def Tick():
    """Required tick function"""
    # Parent.SendStreamMessage('Tick')
    return


def respond(output):
    retVal = output
    # If the original message is from a discord message
    Parent.SendStreamMessage(str(retVal))