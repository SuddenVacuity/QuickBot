'''
This file is subject to the terms and conditions found 
in the file "LICENSE" located in the project base 
'''

import time
import socket

import re
import json

# bring in all the command functions
# needed to register commands
from defaultcommands import *
from customcommands import *

####################################################

# command registry
# name (str): the word the command will be recognized by from chat
# function (callable): the name of the existing function that will
#                        be run when the command is called
# NOTE: the function to be called must exist within commands.py
# registration format: [
#	[name, function],
#	["help", displayHelp]
#]

COMMAND_REGISTRY = [
	# custom commands
	["custom", cmdCustom],
	# default commands
	["cmd", cmdTest], 
	["modcmd", cmdModCmd],
	["admcmd", cmdAdmCmd],
	["kill", cmdKill]
]

####################################################

# maximum rate the bot sends messages to the irc server
RATE = (20/30)

# options are loaded from config.json
# contains data required to connect to the server
CONFIG = None

# used to connect to twitch chat
AUTHKEY = None

# options are loaded from customize.json
CUSTOM_OPTIONS = {
   	"connectmsg": "Hello",
    "disconnectmsg": "Goodbye"
}

# regex pattern and filter
CHAT_MSG_RE = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
WORD_FILTER = [
	r"badword"
]

######
#
#   LOAD CONFIG
#
######

# import config.json options
try:
	with open("config.json", encoding='utf-8') as f:
		CONFIG = json.load(f)
except:
	print("ERROR: Open config.json failed.")
	exit()

# import twitch auth token
# do not put in a dictionary - what if you need to print/log it?
try:
	with open("authkey", encoding='utf-8') as f:
		AUTHKEY = f.read()
except:
	print("ERROR: Open authkey failed.")
	exit()

# import customize.json options
try:
	with open("customize.json", encoding='utf-8') as f:
		data = json.load(f)
		for key in data.keys():
			CUSTOM_OPTIONS[key] = data[key]
except:
	print("WARNING: Open customize.json failed")

####################################################

def chat(sock, msg):
	message = "PRIVMSG {} :{}\r\n".format(CONFIG['channelname'], msg)
	sock.send(message.encode("utf-8"))

def ban(sock, user):
	# send whisper before timeout
	chat(sock, ".w {} you are banned from this channel".format(user, secs))
	chat(sock, ".ban {}".format(user))

def timeout(sock, user, secs=600):
	# send whisper before timeout
	chat(sock, ".w {} you are in timeout for {} seconds".format(user, secs))
	chat(sock, ".timeout {} {}".format(user, secs))

def disconnect(sock):
	chat(sock, CUSTOM_OPTIONS['disconnectmsg'])

	time.sleep(1.5)

	message = "PART {}\r\n".format(CONFIG['channelname'])
	sock.send(message.encode("utf-8"))
	
	exit()

######
#
#   COMMANDS
#
######

# perform internal actions related to a command and its arguments
# returns a string to be sent as a response
# returns None if there should be no reponse
def runCommand(username, command, args):
	response = "Invalid Command by: !{}".format(command)

	# search command registry to see if an existing command was called
	# cmd is a tuple with a command name and a function to be called if names match
	# fuction arguments are (username, args)
	for cmd in COMMAND_REGISTRY:
		if cmd[0] == command:
			response = cmd[1](username, args)

	return response

# sanitize and split a message to be used as a command
# returns a string to be sent as a response
# returns None if there should be no reponse
def processCommand(username, message):
	# remove the end-of-message token from the message
	message = message.rstrip("\r\n")

	# seperate the command from its arguments
	command = message # this will not be changed if there are no arguments
	args = ""

	if(message.find(" ") != -1):
		# the commend had arguments
		msgSplit = message.split(" ", 1)
		command = msgSplit[0]
		args = msgSplit[1]
		
	# remove the leading ! from the command
	command = command.lstrip("!")

	# perform the command and get a response string
	response = runCommand(username, command, args)

	return response

def containsBadLanguage(message):
	for pattern in WORD_FILTER:
		if re.match(pattern, message):
			return True

	return False

###############

# runs for every non-PING message received
def processMessage(sock, username, message):
	# prevent possible infinite loop if the bot somehow gets its own messages
	if username == CONFIG["botname"]:
		return None

	# react to command
	if(message.startswith("!")):
		print("PROCESSING COMMAND - " + username + ": " + message)
		rsp = processCommand(username, message)
		if rsp != None:
			if rsp != KILLCODE: # KILLCODE is stored in commands.py
				chat(sock, rsp)
			else:
				disconnect(sock)
	# scan chat and react to contents
	elif(containsBadLanguage(message) == True):
		chat(sock, "{} said something bad. Shameful!".format(username))

######
#
#   NETWORK IRC CONNECTION
#
######

s = socket.socket()
s.connect((CONFIG['host'], CONFIG['port']))
s.send("PASS {}\r\n".format(AUTHKEY).encode("utf-8"))
s.send("NICK {}\r\n".format(CONFIG['botname']).encode("utf-8"))
s.send("JOIN {}\r\n".format(CONFIG['channelname']).encode("utf-8"))
chat(s, CUSTOM_OPTIONS['connectmsg'])

######
#
#   LISTEN FOR MESSAGES
#
######

# run the bot
while True:
	response = s.recv(1024).decode("utf-8")

	if(response == "PING :tmi.twitch.tv\r\n"):
		s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
	elif response != None:
		# do bot functions here
		username = re.search(r"\w+", response).group(0) # return the entire match
		message = CHAT_MSG_RE.sub("", response)
		processMessage(s, username, message)

	# TODO: find alternative to sleep()
	time.sleep(1 / RATE)
