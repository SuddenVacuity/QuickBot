# QuickBot

## PLANNED FEATURES:
User, moderator and admin levels of command access  
Easily create custom chat functions  
Premade Functions:  
- Automated repeating/updating messages
- Command to save and repeat quotes
- Chat voting

## DEPENDENCIES:
Python 3.7+

## FIRST-USE SETUP:
Navigate to the directory containing chatbox.py.  
In this directory create 4 empty files: config.json, customize.json, authkey and permissions.json.  
Next you will enter data into these files.
### **1. config.json**
The information in this file will tell the bot where to connect and who to connect as.  
Copy the json data below into your new config.json.

    {
        "host": "irc.twitch.tv",
        "port": 6667,
        "botname": "",
        "channelname": ""
    }

You will notice the values for botname and channelname are empty.  
These values are specific to your use of this bot so you must set them.
* **botname:** must be the name of the twitch account that the bot will use.  
* **channelname:** must be the name of the channel the bot will connect to beginning with a #.

ex) if you bot's account name is mybot12345 and you plan to use to bot for `https://www.twitch.tv/mychannel` the lines will look like this.

        "botname": "mybot12345",
        "channelname": "#mychannel"

### **2. authkey**
An oauthkey will allow the bot to access certain features of an account without requiring you to enter your password.  
You must ontain a key from twitch for the account you want access to.  
* Your key will look something like oauth:bbt6890Y789bn6Y8bnby97tv6cre76
* https://dev.twitch.tv/docs/irc/#get-environment-variables recommends using https://twitchapps.com/tmi/ to generate your key.

Paste this key into the authkey file.  
* The key must be the only thing in the file and the file must not have a file extension

### **3. permissions.json - optional**
Mods/Admins are optional but its recommended that you add your channel as an admin.  
Some commands such as disconnecting the bot require admin permission.

This file will list users that have an elevated permission level within the bot.  
The json data inside this file has 2 lists; one for admin-level users and one for moderator-level users.

 Your permissions.json may look something like this.

    {
        "admin": [
            "mychannel"
        ],

        "moderator": [
            "moderator1",
            "moderator2",
            "moderator3"
        ]
    }

### **4. customize.json - optional**
This file contains the connect and disconnect messages for your bot.  
Copy this json data into customize.json and change Hello and Goodbye to the messages you want to display.

    {
        "connectmsg": "Hello",
        "disconnectmsg": "Goodbye"
    }

## USE:
After completing the first-use setup open chatbot.py with Python.

The current built-in commands are limited to:
* **!cmd** - returns a response to show a command was recognized.
* **!modcmd** - returns text recognizing wether or not the caller has mod or admin permission.
* **!admcmd** - returns text recognizing wether or not the caller has admin permission.
* **!custom** - test command to test functions in customcommands.py
* **!kill** - returns the disconnect text and shuts down the bot if the caller is an admin.

NOTE: commands are case-sensitive.

## CUSTOM FUNCTIONS:
Creating a custom function requires some basic knowledge of Python.

To add a custom function to the bot you must create and register your new function.  
Create your function in customcommands.py.

Then in chatbot.py find the variable: COMMAND_REGISTRY.  
It will look like this.

    COMMAND_REGISTRY = [
        ...
    ]

Add a new item to the list on a new line in this format: 

    ["command": functionName],  

If this is added to the end of the list you can leave out the ,
ex) you make a function called cmdMyFunc and want it to be called from chat with !myfunc

    COMMAND_REGISTRY = [
        # custom commands
        ["myfunc", cmdMyFunc],
        ["custom", cmdCustom],
        # default commands
        ["cmd", cmdTest], 
        ["modcmd", cmdModCmd],
        ["admcmd", cmdAdmCmd],
        ["kill", cmdKill]
    ]