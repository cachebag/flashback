from datetime import datetime
from typing import List
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models import Video


class YouTubeClient:
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos_by_year(
        self, 
        query: str, 
        year: int, 
        max_results: int = 50
    ) -> List[Video]:
        try:
            published_after = f"{year}-01-01T00:00:00Z"
            published_before = f"{year + 1}-01-01T00:00:00Z"
            
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                type='video',
                order='relevance',
                publishedAfter=published_after,
                publishedBefore=published_before,
                maxResults=max_results
            ).execute()
            
            videos = []
            video_ids = []
            
            for search_result in search_response.get('items', []):
                video_id = search_result['id']['videoId']
                video_ids.append(video_id)
                
                snippet = search_result['snippet']
                published_at = datetime.fromisoformat(
                    snippet['publishedAt'].replace('Z', '+00:00')
                )
                
                video = Video(
                    video_id=video_id,
                    title=snippet['title'],
                    channel_title=snippet['channelTitle'],
                    description=snippet['description'],
                    published_at=published_at,
                    thumbnail_url=snippet['thumbnails'].get('medium', {}).get('url', '')
                )
                videos.append(video)
            
            if video_ids:
                self._enrich_video_details(videos, video_ids)
            
            return videos
            
        except HttpError as e:
            error_details = e.error_details[0] if e.error_details else {}
            reason = error_details.get('reason', 'Unknown error')
            raise Exception(f"YouTube API error: {reason}")
    
    def _enrich_video_details(self, videos: List[Video], video_ids: List[str]) -> None:
        try:
            video_response = self.youtube.videos().list(
                part='statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            video_details = {
                item['id']: item 
                for item in video_response.get('items', [])
            }
            
            for video in videos:
                details = video_details.get(video.video_id)
                if details:
                    statistics = details.get('statistics', {})
                    view_count = statistics.get('viewCount')
                    if view_count:
                        video.view_count = int(view_count)
                    
                    content_details = details.get('contentDetails', {})
                    duration = content_details.get('duration')
                    if duration:
                        video.duration = self._parse_duration(duration)
                        
        except HttpError:
            # If we can't get additional details, that's okay
            # The basic video info is still valid
            pass
    
    def _parse_duration(self, iso_duration: str) -> str:
        duration = iso_duration[2:]
        
        hours = 0
        minutes = 0
        seconds = 0
        
        if 'H' in duration:
            hours_str, duration = duration.split('H')
            hours = int(hours_str)
        
        if 'M' in duration:
            minutes_str, duration = duration.split('M')
            minutes = int(minutes_str)
        
        if 'S' in duration:
            seconds_str = duration.replace('S', '')
            seconds = int(seconds_str)
        
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}" 
