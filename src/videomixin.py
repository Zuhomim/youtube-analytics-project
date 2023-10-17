from src.apimixin import APIMixin
import json


class VideoMixin(APIMixin):

    @classmethod
    def get_playlist_json(cls, playlist_id):
        """Возвращает словарь плейлиста по его id (playlist_id)"""

        playlist_json = json.dumps(cls.get_service().playlists().list(id=playlist_id,
                                                                      part='snippet,contentDetails',
                                                                      maxResults=50,
                                                                      ).execute(), indent=2)
        return playlist_json

    @classmethod
    def get_playlist(cls, playlist_id):
        playlist = json.loads(cls.get_playlist_json(playlist_id))["items"][0]
        return playlist

    @classmethod
    def get_videos_by_playlist_id(cls, playlist_id) -> dict:
        """Возвращает словарь со всеми видео данного плейлиста"""

        playlist_videos = cls.get_service().playlistItems().list(playlistId=playlist_id,
                                                                 part='contentDetails',
                                                                 maxResults=50,
                                                                 ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        return cls.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
