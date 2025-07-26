import webbrowser
from textual.app import ComposeResult
from textual.containers import ScrollableContainer, Vertical, Center, Middle
from textual.widgets import Button, Label, Static, Footer
from textual.screen import Screen

from ..models import Video


class VideoItem(Static):
    
    def __init__(self, video: Video, **kwargs):
        self.video = video
        super().__init__(**kwargs)
    
    def render(self) -> str:
        title = self.video.title
        if len(title) > 60:
            title = title[:57] + "..."
        
        channel = self.video.channel_title
        if len(channel) > 25:
            channel = channel[:22] + "..."
        
        pub_date = self.video.published_at.strftime("%Y-%m-%d")
        
        view_count = self._format_view_count(self.video.view_count) if self.video.view_count else "N/A"
        duration = self.video.duration if self.video.duration else "N/A"
        
        return f"{title}\n{channel} | {pub_date} | {duration} | {view_count} views"
    
    def _format_view_count(self, count: int) -> str:
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.1f}K"
        else:
            return str(count)
    
    def on_click(self) -> None:
        webbrowser.open(self.video.url)


class ResultsScreen(Screen):
    
    BINDINGS = [
        ("escape", "go_back", "Back"),
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+p", "command_palette", "Command Palette"),
        ("b", "go_back", "Back"),
        ("q", "quit", "Quit"),
    ]
    
    def __init__(self, videos, search_query, year, **kwargs):
        super().__init__(**kwargs)
        self.videos = videos
        self.search_query = search_query
        self.year = year
    
    def compose(self) -> ComposeResult:
        yield Center(
            Middle(
                Vertical(
                    Button("← back", id="back_button"),
                    Label(f"Found {len(self.videos)} videos for '{self.search_query}' from {self.year}"),
                    ScrollableContainer(
                        *[VideoItem(video) for video in self.videos] if self.videos else [Label("No videos found. Try different search terms or year.")],
                        id="results_scroll"
                    ),
                    id="results_container"
                )
            )
        )
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back_button":
            self.app.pop_screen()
    
    def action_go_back(self) -> None:
        self.app.pop_screen() 
