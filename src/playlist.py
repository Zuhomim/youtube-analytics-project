import isodate
from datetime import timedelta
from src.apimixin import APIMixin
import json


class PlayList(APIMixin):

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id

        self.title = self.get_playlist(playlist_id)["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.__total_duration = self.get_total_duration()

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

    def show_best_video(self) -> str:
        """Возвращает video-dict с максимальным likeCount"""

        video_list = self.get_videos_by_playlist_id(self.playlist_id)["items"]
        best_video = max(video_list, key=lambda video: int(video["statistics"]["likeCount"]))

        return f'https://youtu.be/{best_video["id"]}'

    @property
    def total_duration(self) -> timedelta:
        return self.__total_duration

    def get_total_duration(self) -> timedelta:
        """Возвращает общую длительность видео данного плейлиста"""

        # Сумма времени продолжительности всех видео в плейлисте
        duration = timedelta()
        # Словарь плейлиста - items содержит список видео
        video_response = self.get_videos_by_playlist_id(self.playlist_id)

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']

            duration += isodate.parse_duration(iso_8601_duration)
        return duration

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в виде JSON с отступом (indent = 2)"""

        playlist = self.get_playlist_json(self.playlist_id)
        print(playlist)
