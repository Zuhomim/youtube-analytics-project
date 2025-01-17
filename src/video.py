from src.apimixin import APIMixin
import json


class Video(APIMixin):
    """Класс для видео на Youtube"""

    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        # try:
        video_json = json.dumps(self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                                 id=video_id
                                                                 ).execute())
        try:
            video = json.loads(video_json)["items"][0]
        except IndexError:
            self.video_title = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None
            self.url = None
        else:
            self.video_title = video['snippet']['title']
            self.view_count = video['statistics']['viewCount']
            self.like_count = video['statistics']['likeCount']
            self.comment_count = video['statistics']['commentCount']
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'

    def __str__(self):
        return f'{self.video_title}'


class PLVideo(Video):
    """Класс, наследуемый от Video для видео с конкретного плейлиста Youtube"""

    def __init__(self, video_id: str, playlist_id: str) -> None:
        super().__init__(video_id)
        self.playlist_id = playlist_id
