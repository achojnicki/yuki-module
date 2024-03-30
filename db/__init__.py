from pymongo import MongoClient

class DB:
	def __init__(self, root):
		self._root=root
		self._config=root._config

		self._mongo_cli = MongoClient(
			self._config.mongo.host,
			self._config.mongo.port
		)

		self._mongo_db = self._mongo_cli[self._config.mongo.db]
		self._videos_collection=self._mongo_db['videos']


	def get_video(self, video_uuid):
		query={"video_uuid": video_uuid}
		return self._videos_collection.find_one(query)

	def create_video(self, video_uuid, video_title, video_description):
		document={
			"video_uuid": str(video_uuid),
			"video_title": video_title,
			"video_description": video_description,
			"status": "pending",
			"images_ready": False,
			"speech_ready": False
		}
		self._videos_collection.insert_one(document)

	def update_video(self, video_uuid, video, typ):
		query={"video_uuid": video_uuid}
		data=self._videos_collection.find_one(query)

		for scene in data['script']:
			index=data['script'].index(scene)
			data['script'][index][typ]=video['script'][index][typ]


		if typ=='image':
			rep_query={"$set": {"script": data['script'],'images_ready':True }}
		else:
			rep_query={"$set": {"script": data['script'],'speech_ready':True }}


		self._videos_collection.update_one(
			query,
			rep_query
		)