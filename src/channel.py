import json
from src.constants import youtube


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале в виде JSON с отступом (indent = 2)"""

        channel = json.dumps(youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute(), indent=2)
        print(channel)
