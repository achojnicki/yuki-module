from moviepy import editor
from pathlib import Path
from math import ceil

class Scene_Wobbling_Grow:
	def __init__(
		self,
		root,
		image:Path,
		audio:Path,
		audio_volume:float=0.8,
		start_image_width:int=900,
		max_image_width:int=1000,
		end_margin:int=2,
		**kwargs
		):

		self._root=root

		self._image=str(image)
		self._start_image_width=start_image_width
		self._max_image_width=max_image_width

		self._audio=str(audio)
		self._audio_volume=audio_volume

		self._end_margin=end_margin

		self._background_image_clip=editor.ImageClip(self._root._background_image)
		
		self._audio_clip=editor.AudioFileClip(self._audio).volumex(self._audio_volume)
		self._audio_clip=self._audio_clip.subclip(0, self._audio_clip.duration-0.06)

		self._image_clip=editor.ImageClip(
			self._image
			).set_position('center').set_fps(self._root._fps).set_duration(self._audio_clip.duration+self._end_margin).resize(width=self._animation)


	@property
	def clip(self):
		return editor.CompositeVideoClip(
			[self._background_image_clip, self._image_clip],
			size=self._root._video_size
			).set_duration(self._audio_clip.duration+self._end_margin).set_audio(self._audio_clip)


	def _animation(self, time):
		if time==0:
			return self._start_image_width
		else:
			return self._start_image_width+int(round(time/self._audio_clip.duration*(self._max_image_width-self._start_image_width), 2))
				


	def _animation(self, time):
		if time==0:
			return self._start_image_width
		else:
			return self._start_image_width+int(round(time/self._audio_clip.duration*(self._max_image_width-self._start_image_width), 2))
				


