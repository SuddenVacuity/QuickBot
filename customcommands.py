'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base 
'''

from defaultcommands import *

# create a function for each command here
# NOTE: the command must be registered in chatbot.py to be recognized
# NOTE: all functions must take the arguments (username, args)
# username (str): the name of the user that called th command
# args (str): all text after the initial command

def cmdCustom(username, args):
	if(hasAdminAccess(username) == True):
		return "An admin called a custom command."
	if(hasModAccess(username) == True):
		return "A moderator called a custom command."

	return "A viewer called a custom command."