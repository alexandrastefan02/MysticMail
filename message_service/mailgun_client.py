import os
import requests
def send_simple_message(recv, message):
  	return requests.post(
  		"https://api.mailgun.net/v3/sandbox263864b346494381bef10298659bd257.mailgun.org/messages",
  		auth=("api", "b776b34ab85679a85d9af5bd7b5dfb6c-10b6f382-cb1cfa88"),
  		data={"from": "Mailgun Sandbox <postmaster@sandbox263864b346494381bef10298659bd257.mailgun.org>",
			"to": "<"+recv+">",
  			"subject": "MysticMail Message",
  			"text": message})