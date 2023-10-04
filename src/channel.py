import json
from src.constants import youtube


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        channel_json = json.dumps(youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
                                  indent=2)
        channel = json.loads(channel_json)["items"][0]
        self.description = channel["snippet"]["description"]
        self.title = channel["snippet"]["title"]
        self.video_count = channel["statistics"]["videoCount"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.view_count = channel["statistics"]["viewCount"]
        self.subscriber_count = channel["statistics"]["subscriberCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в виде JSON с отступом (indent = 2)"""

        channel = json.dumps(youtube.channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
                             indent=2)
        print(channel)

    @property
    def channel_id(self):
        """геттер атрибута channel_id"""

        return self.__channel_id

    @classmethod
    def get_service(cls):
        """возвращает объект для работы с Youtube API"""

        return youtube

    def to_json(self, json_path):
        """записывает объект с channel_info в файл json"""

        channel_info = {
            "channel_id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber_count": self.subscriber_count,
            "video_count": self.video_count,
            "view_count": self.view_count
        }
        print(channel_info)
        with open(json_path, 'w') as data_json:
            data_json.write(json.dumps(channel_info, indent=4, ensure_ascii=False))
