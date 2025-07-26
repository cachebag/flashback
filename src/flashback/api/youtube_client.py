import os
from datetime import datetime, timezone
from typing import List, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from ..models import Video


class YouTubeClient:
    """Client for interacting with the YouTube Data API."""
    
    def __init__(self, api_key: str):
        """Initialize the YouTube client.
        
        Args:
            api_key: YouTube Data API key
        """
        self.api_key = api_key
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def search_videos_by_year(
        self, 
        query: str, 
        year: int, 
        max_results: int = 50
    ) -> List[Video]:
        """Search for videos from a specific year.
        
        Args:
            query: Search query string
            year: Year to search within
            max_results: Maximum number of results to return
            
        Returns:
            List of Video objects matching the search criteria
            
        Raises:
            HttpError: If there's an issue with the API request
        """
        try:
            # Create date range for the specified year
            published_after = f"{year}-01-01T00:00:00Z"
            published_before = f"{year + 1}-01-01T00:00:00Z"
            
            # Search for videos
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
            
            # Extract video IDs and basic info
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
            
            # Get additional video details (duration, view count)
            if video_ids:
                self._enrich_video_details(videos, video_ids)
            
            return videos
            
        except HttpError as e:
            error_details = e.error_details[0] if e.error_details else {}
            reason = error_details.get('reason', 'Unknown error')
            raise Exception(f"YouTube API error: {reason}")
    
    def _enrich_video_details(self, videos: List[Video], video_ids: List[str]) -> None:
        """Enrich video objects with additional details like duration and view count.
        
        Args:
            videos: List of Video objects to enrich
            video_ids: List of video IDs to get details for
        """
        try:
            # Get video statistics and content details
            video_response = self.youtube.videos().list(
                part='statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            # Create a mapping of video ID to details
            video_details = {
                item['id']: item 
                for item in video_response.get('items', [])
            }
            
            # Update video objects with additional details
            for video in videos:
                details = video_details.get(video.video_id)
                if details:
                    # Add view count
                    statistics = details.get('statistics', {})
                    view_count = statistics.get('viewCount')
                    if view_count:
                        video.view_count = int(view_count)
                    
                    # Add duration
                    content_details = details.get('contentDetails', {})
                    duration = content_details.get('duration')
                    if duration:
                        video.duration = self._parse_duration(duration)
                        
        except HttpError:
            # If we can't get additional details, that's okay
            # The basic video info is still valid
            pass
    
    def _parse_duration(self, iso_duration: str) -> str:
        """Parse ISO 8601 duration format to a readable string.
        
        Args:
            iso_duration: Duration in ISO 8601 format (e.g., 'PT4M13S')
            
        Returns:
            Human-readable duration string (e.g., '4:13')
        """
        # Remove 'PT' prefix
        duration = iso_duration[2:]
        
        # Initialize time components
        hours = 0
        minutes = 0
        seconds = 0
        
        # Parse hours
        if 'H' in duration:
            hours_str, duration = duration.split('H')
            hours = int(hours_str)
        
        # Parse minutes
        if 'M' in duration:
            minutes_str, duration = duration.split('M')
            minutes = int(minutes_str)
        
        # Parse seconds
        if 'S' in duration:
            seconds_str = duration.replace('S', '')
            seconds = int(seconds_str)
        
        # Format duration string
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            return f"{minutes}:{seconds:02d}" 