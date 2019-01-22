'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base 
'''

# import permissions
import json
PERMISSIONS = {}
try:
	with open("permissions.json", encoding='utf-8') as f:
		PERMISSIONS = json.load(f)
except:
	print("WARNING: Open permissions.json failed")


keys = PERMISSIONS.keys()
if "admin" not in keys:
	PERMISSIONS["admin"] = []
if "moderator" not in keys:
	PERMISSIONS["moderator"] = []

# this is returned is a command is called by someone that doens't have permision to do so
permissionError = "You aren't authorized to do that"

# if this value is returned by a command the bot will shutdown
KILLCODE = "Bf9.8*UN0v34^6;v"

# create a function for each command here
# NOTE: the command must be registered in chatbot.py to be recognized
# NOTE: all functions must take the arguments (username, args)
# username (str): the name of the user that called th command
# command (str): the command that was called
# args (str): all text after the initial command

# returns True if the callers name matches a name in the admin list
def hasAdminAccess(username):
	if username in PERMISSIONS["admin"]:
		return True
	return False

# returns True if the callers name matches a name in the moderator OR admin list
def hasModAccess(username):
	if hasAdminAccess(username) == True:
		return True
	if username in PERMISSIONS["moderator"]:
		return True
	return False

# runs when "test" is called
def cmdTest(username, args):
	return "a command was run by {}".format(username) 

# test mod/admin permission
def cmdModCmd(username, args):
	if hasModAccess(username) == False:
		return "{} {}.".format(permissionError, username)

	return "You have permission to do this {}".format(username) 

# test admin permission
def cmdAdmCmd(username, args):
	if hasAdminAccess(username) == False:
		return "{} {}.".format(permissionError, username)

	return "You have permission to do this {}".format(username) 

# the bot sends the disconnect message then exits
def cmdKill(username, args):
	if hasAdminAccess(username) == False:
		return "{} {}.".format(permissionError, username)

	return KILLCODE