#!/bin/bash
if [ "pgrep -f /usr/bin/python3.6 /home/admi/bot/bot-file.py"]
	then {
		echo "Exit! Python bot is already running!"
		exit 1
	}
else
	{
		sleep 1  #delay
                /usr/bin/python3.6 /home/admi/bot/bot-file.py
                exit 1
	}
fi;
