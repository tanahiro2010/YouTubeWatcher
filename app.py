from yt_dlp import YoutubeDL
from googleapiclient.discovery import build
import json

class YouTube:
    def __init__(self, api_token: str):
        self.download_data = {
            'format': 'best',
            'outtmpl': '',
        }

        self.youtube = build('youtube', 'v3', developerKey=api_token)
        self.video_base_url = 'https://www.youtube.com/watch?v='

    def download_youtube_video(self, video_id: str):
        self.download_data['outtmpl'] = '{}.mp4'.format(video_id)
        url = self.video_base_url + video_id
        print('URL: {}'.format(url))
        print('Downloading video...')

        with YoutubeDL(self.download_data) as ydl:
            ydl.download([self.video_base_url + video_id])

        return self.download_data['outtmpl']

    def investigate_video(self, query: str = ""):
        response = self.youtube.search().list(
            part='snippet,id',
            type='video',
            maxResults=100,
            q=query
        ).execute()

        videos_data = []

        for item in response['items']:
            snippet = item['snippet']
            video_data = {
                'title': snippet['title'],
                'description': snippet['description'],
                'thumbnail': snippet['thumbnails']['high']['url'],
                'video_id': item['id']['videoId']
            }

            videos_data.append(video_data)

        return videos_data

    def fetch_video(self, video_id: str):
        response = self.youtube.videos().list(
            part='snippet,statistics',
            id=video_id
        ).execute()

        for item in response.get("items", []):
            if item["kind"] != "youtube#video":
                continue
            return item

