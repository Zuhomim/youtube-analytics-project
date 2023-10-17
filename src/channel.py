import json

from src.apimixin import APIMixin


class Channel(APIMixin):
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = (self.get_service().channels().list(id=channel_id, part='snippet,statistics')
                   .execute())["items"][0]

        self.description = channel["snippet"]["description"]
        self.title = channel["snippet"]["title"]
        self.video_count = channel["statistics"]["videoCount"]
        self.url = f'https://www.youtube.com/channel/{self.__channel_id}'
        self.view_count = channel["statistics"]["viewCount"]
        self.subscriber_count = channel["statistics"]["subscriberCount"]
        self.subscriber_count_int = int(self.subscriber_count)

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Складывать можно только два объекта Channel.')
        else:
            return self.subscriber_count_int + other.subscriber_count_int

    def __sub__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Вычислять разницу можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int - other.subscriber_count_int

    def __gt__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Проверять сравнение gt можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int > other.subscriber_count_int

    def __ge__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Проверять сравнение ge можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int >= other.subscriber_count_int

    def __lt__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Проверять сравнение lt можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int < other.subscriber_count_int

    def __le__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Проверять сравнение le можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int <= other.subscriber_count_int

    def __eq__(self, other):
        if not isinstance(other, Channel):
            raise ValueError('Проверять равенство можно только для двух объектов Channel.')
        else:
            return self.subscriber_count_int == other.subscriber_count_int

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в виде JSON с отступом (indent = 2)"""

        channel_json = json.dumps(
            self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute(),
            indent=2)
        print(channel_json)

    @property
    def channel_id(self):
        """геттер атрибута channel_id"""

        return self.__channel_id

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
        with open(json_path, 'w') as fp:
            json.dump(channel_info, fp, indent=4, ensure_ascii=False)
