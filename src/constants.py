import os
from googleapiclient.discovery import build

# API-key из переменных окружения
api_key: str = os.getenv('YOUTUBE_API_KEY')

# Объект для работы с Youtube
youtube = build('youtube', 'v3', developerKey=api_key)
