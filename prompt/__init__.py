from json import loads, dumps
from pprint import pprint

class Prompt:
	def __init__(self):
		pass
	
	def build(self, system_message, video_title, video_description, format_example):
		msg=[]

		msg.append(
			{
				"role": "system",
				"content": system_message
			}
		)

		msg.append(
			{
				"role": "user",
				"content": video_title
			}
		)

		msg.append(
			{
				"role": "user",
				"content": video_description
			}
		)

		msg.append(
			{
				"role": "user",
				"content": format_example
			}
		)
		
		return msg