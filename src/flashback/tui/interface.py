import os
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.widgets import Input, Button, Label, Select, Footer

from ..api import YouTubeClient
from ..utils import load_config
from .results import ResultsScreen


class FlashbackTUI(App):

    CSS_PATH = os.path.join(os.path.dirname(__file__), "styles.tcss")
    
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("ctrl+s", "search", "Search"),
        ("ctrl+c", "clear_search", "Clear Search"),
        ("ctrl+p", "command_palette", "Command Palette"),
        ("ctrl+t", "toggle_theme", "Toggle Theme"),
        ("f1", "help", "Help"),
    ]
    
    def __init__(self):
        super().__init__()
        self.enable_command_palette = True
        try:
            config = load_config()
            self.youtube_client = YouTubeClient(config['youtube_api_key'])
        except ValueError as e:
            self.youtube_client = None
            self.error_message = str(e)
    
    def compose(self) -> ComposeResult:
        if not self.youtube_client:
            yield Center(
                Middle(
                    Label(f"Configuration Error: {self.error_message}")
                )
            )
            return
        
        current_year = datetime.now().year
        year_options = [(str(year), year) for year in range(current_year, 2004, -1)]
        results_options = [
            ("10 results", 10),
            ("25 results", 25),
            ("50 results", 50)
        ]
        
        theme_options = [
            ("Dark", "textual-dark"),
            ("Light", "textual-light"),
            ("Gruvbox", "gruvbox"),
            ("Dracula", "dracula"),
            ("Nord", "nord"),
            ("Monokai", "monokai"),
            ("Tokyo Night", "tokyo-night"),
            ("Catppuccin", "catppuccin-mocha"),
        ]
        
        yield Center(
            Middle(
                Vertical(
                    Label("flashback"),
                    Input(placeholder="Enter your search query...", id="search_input"),
                    Select(year_options, value=current_year, id="year_select"),
                    Select(results_options, value=25, id="results_select"),
                    Select(theme_options, value="textual-dark", id="theme_select", prompt="Select Theme"),
                    Button("Search", variant="primary", id="search_button"),
                    Label("", id="status"),
                    id="search_form"
                )
            )
        )
        yield Footer()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_button":
            self.perform_search()
    
    def on_select_changed(self, event: Select.Changed) -> None:
        if event.select.id == "theme_select":
            self.theme = event.value
            status_label = self.query_one("#status", Label)
            status_label.update(f"🎨 Theme changed to {event.value}")
            self.set_timer(1.5, lambda: self.clear_theme_status())
    
    def clear_theme_status(self) -> None:
        try:
            status_label = self.query_one("#status", Label)
            status_label.update("")
        except:
            pass
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "search_input":
            self.perform_search()
    
    def on_screen_resume(self) -> None:
        try:
            status_label = self.query_one("#status", Label)
            status_label.update("")
        except:
            pass
    
    def perform_search(self) -> None:
        search_input = self.query_one("#search_input", Input)
        year_select = self.query_one("#year_select", Select)
        results_select = self.query_one("#results_select", Select)
        
        query = search_input.value.strip()
        if not query:
            return
        
        year = year_select.value
        max_results = results_select.value
        
        status_label = self.query_one("#status", Label)
        status_label.update("🔍 Searching...")
        
        self.run_worker(self._search_worker(query, year, max_results), exclusive=True)
    
    async def _search_worker(self, query: str, year: int, max_results: int) -> None:
        try:
            videos = self.youtube_client.search_videos_by_year(query, year, max_results)
            try:
                status_label = self.query_one("#status", Label)
                status_label.update("")
            except:
                pass
            self.push_screen(ResultsScreen(videos, query, year))
        except Exception as e:
            try:
                status_label = self.query_one("#status", Label)
                status_label.update(f"❌ Error: {str(e)}")
            except:
                pass
    
    def action_search(self) -> None:
        self.perform_search()
    
    def action_clear_search(self) -> None:
        try:
            search_input = self.query_one("#search_input", Input)
            search_input.value = ""
            search_input.focus()
            status_label = self.query_one("#status", Label)
            status_label.update("🧹 Search cleared")
            self.set_timer(1.0, lambda: self.clear_status())
        except:
            pass
    
    def action_toggle_theme(self) -> None:
        try:
            theme_select = self.query_one("#theme_select", Select)
            current_theme = theme_select.value
            new_theme = "textual-light" if current_theme == "textual-dark" else "textual-dark"
            theme_select.value = new_theme
            self.theme = new_theme
            status_label = self.query_one("#status", Label)
            status_label.update(f"🎨 Theme switched to {new_theme}")
            self.set_timer(1.5, lambda: self.clear_status())
        except:
            pass
    
    def action_help(self) -> None:
        try:
            status_label = self.query_one("#status", Label)
            status_label.update("💡 Enter search query → Select year → Press Enter or Ctrl+S to search")
            self.set_timer(3.0, lambda: self.clear_status())
        except:
            pass
    
    def clear_status(self) -> None:
        try:
            status_label = self.query_one("#status", Label)
            status_label.update("")
        except:
            pass


def run_tui():
    app = FlashbackTUI()
    app.run()


if __name__ == "__main__":
    run_tui() 