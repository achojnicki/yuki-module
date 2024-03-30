from yuki.script.constants import SYSTEM_MESSAGE

from openai import OpenAI
class Script:
	def __init__(self, root):
		self._root=root
		self._config=root._config
		
		self._openai_cli=OpenAI()

