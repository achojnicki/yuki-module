from yuki.video.scenes import Scene_Static, Scene_Zoom_In


from moviepy import editor
from pathlib import Path

class UnknownSceneType(Exception):
	pass

class EP:
	_scenes_types=[
		Scene_Static,
		Scene_Zoom_In
		]
	def __init__(
		self,
		video_file:str,
		video_size:tuple or list,
		background_image:Path,
		background_audio:Path=None,
		background_audio_volume:float=0.05,
		fps:int=60
		):

		self._video_file=str(video_file)
		self._video_size=video_size
		self._background_image=str(background_image)
		self._background_audio=str(background_audio)
		self._background_audio_volume=background_audio_volume
		self._fps=fps

		self._scenes=[]


	@property
	def _audio_loops(self):
		x=round(self._main_clip.duration/self._background_audio_clip.duration)
		if x==0:
			x+=1
		return x
		
	@property
	def _audio_duration(self):
		if self._background_audio_clip.duration>self._main_clip.duration:
			return self._main_clip.duration

	def _set_main_clip(self):

		self._main_clip=editor.concatenate_videoclips(
			[scene.clip for scene in self._scenes],
			)

		if self._background_audio:
			self._background_audio_clip=editor.AudioFileClip(self._background_audio).volumex(self._background_audio_volume)
			self._background_audio_clip=self._background_audio_clip.audio_loop(self._audio_loops)
			self._background_audio_clip=self._background_audio_clip.subclip(0, self._background_audio_clip.duration-0.05)
			self._background_audio_clip=self._background_audio_clip.audio_fadein(0.01)
			self._background_audio_clip=self._background_audio_clip.audio_fadeout(0.01)	
			self._background_audio_clip=self._background_audio_clip.set_duration(self._audio_duration)

			self._audio_clip=editor.CompositeAudioClip([self._main_clip.audio, self._background_audio_clip])
			self._main_clip=self._main_clip.set_audio(self._audio_clip)
	
	def add_scene(self, scene, image, **kwargs):
		if scene not in self._scenes_types:
			raise UnknownSceneType

		self._scenes.append(
			scene(root=self, image=image, **kwargs)
			)

	def render(self):
		self._set_main_clip()
		self._main_clip.write_videofile(self._video_file, fps=self._fps, audio_codec='aac')



