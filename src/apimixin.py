import os
from googleapiclient.discovery import build


class APIMixin:
    __API_KEY: str = os.getenv('YOUTUBE_API_KEY')

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.__API_KEY)
