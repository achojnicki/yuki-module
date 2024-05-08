class BGM:
	def __init__(self, root):
		self._root=root
		self._config=root._config


		self._media_dir=root._media_dir
		self._bgm=1


	@property
	def background_audio_intro(self):
		return str(self._media_dir.joinpath(f'bgm/bgm_{self._bgm}/intro.wav'))

	@property
	def background_audio_loop(self):
		return str(self._media_dir.joinpath(f'bgm/bgm_{self._bgm}/loop.wav'))

	def set_bgm(self, bgm:int):
		self._bgm=bgm