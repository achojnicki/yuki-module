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
		background_audio_intro:Path=None,
		background_audio_loop:Path=None,
		background_audio_volume:float=0.1,
		fps:int=60
		):

		self._video_file=str(video_file)
		self._video_size=video_size
		self._background_image=str(background_image)
		self._background_audio_intro=str(background_audio_intro)
		self._background_audio_loop=str(background_audio_loop)
		self._background_audio_volume=background_audio_volume
		self._fps=fps

		self._scenes=[]


	@property
	def _audio_loops(self):
		x=round(self._main_clip.duration/self._background_audio_loop_clip.duration)
		if x==0:
			x+=1
		return x
		
	@property
	def _audio_duration(self):
		return self._main_clip.duration

	def _set_main_clip(self):

		self._main_clip=editor.concatenate_videoclips(
			[scene.clip for scene in self._scenes],
			)

		if self._background_audio_intro and self._background_audio_loop:
			self._background_audio_intro_clip=editor.AudioFileClip(self._background_audio_intro)
			self._background_audio_intro_clip=self._background_audio_intro_clip.subclip(0, self._background_audio_intro_clip.duration-0.05)

			self._background_audio_loop_clip=editor.AudioFileClip(self._background_audio_loop)
			#self._background_audio_loop_clip=self._background_audio_loop_clip.subclip(0, self._background_audio_loop_clip.duration-0.05)
			self._background_audio_loop_clip=self._background_audio_loop_clip.audio_loop(self._audio_loops)

			self._background_audio_clip=editor.concatenate_audioclips(
				[self._background_audio_intro_clip, self._background_audio_loop_clip]
				)
			self._background_audio_clip=self._background_audio_clip.audio_normalize().volumex(self._background_audio_volume)

			#self._background_audio_clip=self._background_audio_clip.subclip(0, self._background_audio_clip.duration-0.05)
			self._background_audio_clip=self._background_audio_clip.set_duration(self._audio_duration)

			self._audio_clip=editor.CompositeAudioClip([self._main_clip.audio, self._background_audio_clip])
			self._audio_clip=self._audio_clip.audio_fadeout(0.01)

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


