from yuki.video.zoom import Zoom

from moviepy import editor
from pathlib import Path

class Scene_Zoom_In:
	def __init__(
		self,
		root,
		image:Path,
		audio:Path,
		audio_volume:float=0.8,
		image_width:int=900,
		zoom_in_speed:int=1.2,
		end_margin:int=2,
		**kwargs
		):

		self._root=root

		self._image=str(image)
		self._image_width=image_width
		self._zoom_in_speed=zoom_in_speed

		self._audio=str(audio)
		self._audio_volume=audio_volume

		self._end_margin=end_margin

		self._background_image_clip=editor.ImageClip(self._root._background_image)
		
		self._audio_clip=editor.AudioFileClip(self._audio).volumex(self._audio_volume)
		self._audio_clip=self._audio_clip.subclip(0, self._audio_clip.duration-0.06)

		self._image_clip=editor.ImageClip(
			self._image
			).set_position('center').set_fps(self._root._fps).set_duration(self._audio_clip.duration+self._end_margin).resize(width=self._image_width)

		self._image_clip=Zoom(self._image_clip, mode='in', position='center', speed=self._zoom_in_speed)


	@property
	def clip(self):
		return editor.CompositeVideoClip(
			[self._background_image_clip, self._image_clip],
			size=self._root._video_size
			).set_duration(self._audio_clip.duration+self._end_margin).set_audio(self._audio_clip)