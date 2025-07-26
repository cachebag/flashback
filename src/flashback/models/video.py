"""
Video model for representing YouTube video data.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Video:
    
    video_id: str
    title: str
    channel_title: str
    description: str
    published_at: datetime
    thumbnail_url: str
    duration: Optional[str] = None
    view_count: Optional[int] = None
    
    @property
    def url(self) -> str:
        return f"https://www.youtube.com/watch?v={self.video_id}"
    
    @property
    def published_year(self) -> int:
        return self.published_at.year
    
    def __str__(self) -> str:
        return f"{self.title} by {self.channel_title} ({self.published_year})" 