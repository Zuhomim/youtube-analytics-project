import isodate
from datetime import timedelta
from src.videomixin import VideoMixin


class PlayList(VideoMixin):

    def __init__(self, playlist_id: str) -> None:
        self.playlist_id = playlist_id

        self.title = self.get_playlist(playlist_id)["snippet"]["title"]
        self.url = f'https://www.youtube.com/playlist?list={playlist_id}'
        self.total_duration = self.get_total_duration()

    def show_best_video(self) -> str:
        """Возвращает video-dict с максимальным likeCount"""

        video_list = super().get_videos_by_playlist_id(self.playlist_id)["items"]
        best_video = max(video_list, key=lambda video: int(video["statistics"]["likeCount"]))

        return f'https://youtu.be/{best_video["id"]}'

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
