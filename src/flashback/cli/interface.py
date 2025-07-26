from datetime import datetime
import click
from colorama import init, Fore, Style
from tabulate import tabulate
from typing import List

from ..api import YouTubeClient
from ..models import Video
from ..utils import load_config, setup_api_key_interactive

init()


class YouTubeSearchCLI:
    
    def __init__(self):
        config = load_config()
        
        if not config.get('has_api_key'):
            click.echo(f"{Fore.YELLOW}No YouTube API key found.{Style.RESET_ALL}")
            try:
                config = load_config()
            except (KeyboardInterrupt, click.Abort):
                click.echo(f"\n{Fore.RED}Setup cancelled. Cannot proceed without API key.{Style.RESET_ALL}")
                raise click.Abort()
        
        try:
            self.youtube_client = YouTubeClient(config['youtube_api_key'])
            self._show_welcome_message()
        except Exception as e:
            click.echo(f"{Fore.RED}Error initializing YouTube client: {e}{Style.RESET_ALL}")
            raise click.Abort()
    
    def _show_welcome_message(self):
        click.echo(f"{Fore.CYAN}🎬 YouTube Archive Searcher{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Find older YouTube videos that algorithms hide.{Style.RESET_ALL}")
        click.echo(f"\n{Fore.BLUE}📊 API Info:{Style.RESET_ALL}")
        click.echo(f"• YouTube API has a daily quota of 10,000 units")
        click.echo(f"• Each search uses ~100 units (≈100 searches/day)")
        click.echo(f"• The API is free but rate-limited")
        click.echo(f"• Type 'quit' or 'exit' to end the session")
        click.echo(f"• Type 'api' to update your API key\n")
    
    def interactive_mode(self):
        
        while True:
            try:
                query = click.prompt(
                    f"{Fore.CYAN}Enter your search query (or 'api' to update API key){Style.RESET_ALL}",
                    type=str
                ).strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    click.echo(f"\n{Fore.GREEN}Thanks for using YouTube Archive Searcher! 🎬{Style.RESET_ALL}")
                    break
                
                if query.lower() in ['api', 'apikey', 'api-key', 'key']:
                    self.update_api_key_interactive()
                    continue
                
                year = click.prompt(
                    f"{Fore.CYAN}Enter the year to search (2005-2024){Style.RESET_ALL}",
                    type=int
                )
                
                max_results = click.prompt(
                    f"{Fore.CYAN}Max results (1-50, default: 25){Style.RESET_ALL}",
                    type=int,
                    default=25,
                    show_default=True
                )
                
                if not self._validate_inputs(year, max_results):
                    continue
                
                self.search_and_display(query, year, max_results)
                
                click.echo(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
                if not click.confirm(f"{Fore.GREEN}Search again?{Style.RESET_ALL}", default=True):
                    click.echo(f"\n{Fore.GREEN}Thanks for using YouTube Archive Searcher! 🎬{Style.RESET_ALL}")
                    break
                    
                click.echo()
                
            except (KeyboardInterrupt, click.Abort):
                click.echo(f"\n\n{Fore.GREEN}Thanks for using YouTube Archive Searcher! 🎬{Style.RESET_ALL}")
                break
            except Exception as e:
                click.echo(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")
                if not click.confirm(f"{Fore.YELLOW}Continue anyway?{Style.RESET_ALL}", default=True):
                    break
    
    def update_api_key_interactive(self):
        try:
            click.echo(f"\n{Fore.CYAN}🔑 Update YouTube API Key{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Current API key will be replaced with the new one.{Style.RESET_ALL}")
            
            if not click.confirm(f"{Fore.BLUE}Do you want to continue?{Style.RESET_ALL}", default=True):
                click.echo(f"{Fore.YELLOW}API key update cancelled.{Style.RESET_ALL}")
                return
            
            api_key = setup_api_key_interactive()
            
            try:
                self.youtube_client = YouTubeClient(api_key)
                click.echo(f"\n{Fore.GREEN}✅ API key updated and client reinitialized successfully!{Style.RESET_ALL}")
            except Exception as e:
                click.echo(f"\n{Fore.RED}❌ Error with new API key: {e}{Style.RESET_ALL}")
                click.echo(f"{Fore.YELLOW}The API key was saved but there might be an issue with it.{Style.RESET_ALL}")
                
        except (KeyboardInterrupt, click.Abort):
            click.echo(f"\n{Fore.YELLOW}API key update cancelled.{Style.RESET_ALL}")
        except Exception as e:
            click.echo(f"\n{Fore.RED}Error updating API key: {e}{Style.RESET_ALL}")
    
    def _validate_inputs(self, year: int, max_results: int) -> bool:
        current_year = datetime.now().year
        if year < 2005 or year > current_year:
            click.echo(f"{Fore.RED}❌ Please enter a year between 2005 and {current_year}.{Style.RESET_ALL}")
            return False
        
        if max_results < 1 or max_results > 50:
            click.echo(f"{Fore.RED}❌ Max results must be between 1 and 50.{Style.RESET_ALL}")
            return False
            
        return True
    
    def search_and_display(self, query: str, year: int, max_results: int = 50) -> None:
        try:
            click.echo(f"\n{Fore.CYAN}Searching for '{query}' from {year}...{Style.RESET_ALL}")
            click.echo(f"{Fore.YELLOW}Please wait, this may take a moment...{Style.RESET_ALL}\n")
            
            videos = self.youtube_client.search_videos_by_year(query, year, max_results)
            
            if not videos:
                click.echo(f"{Fore.YELLOW}No videos found for '{query}' from {year}.{Style.RESET_ALL}")
                click.echo(f"{Fore.BLUE}Try:\n- Different search terms\n- A different year\n- Checking your spelling{Style.RESET_ALL}")
                return
            
            self._display_results(videos, query, year)
            
        except Exception as e:
            click.echo(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    
    def _display_results(self, videos: List[Video], query: str, year: int) -> None:
        click.echo(f"{Fore.GREEN}Found {len(videos)} videos for '{query}' from {year}:{Style.RESET_ALL}\n")
        
        table_data = []
        for i, video in enumerate(videos, 1):
            title = video.title[:60] + "..." if len(video.title) > 60 else video.title
            channel = video.channel_title[:25] + "..." if len(video.channel_title) > 25 else video.channel_title
            
            pub_date = video.published_at.strftime("%Y-%m-%d")
            
            view_count = self._format_view_count(video.view_count) if video.view_count else "N/A"
            
            duration = video.duration if video.duration else "N/A"
            
            table_data.append([
                i,
                title,
                channel,
                pub_date,
                duration,
                view_count
            ])
        
        headers = ["#", "Title", "Channel", "Published", "Duration", "Views"]
        click.echo(tabulate(table_data, headers=headers, tablefmt="grid"))
        
        click.echo(f"\n{Fore.CYAN}Video URLs:{Style.RESET_ALL}")
        for i, video in enumerate(videos, 1):
            click.echo(f"{Fore.BLUE}{i:2d}.{Style.RESET_ALL} {video.url}")
        
        click.echo(f"\n{Fore.GREEN}💡 Tip: On MacOS you can do CMD + click on any URL above to watch the video. {Style.RESET_ALL}")
        
        estimated_quota = len(videos) * 2 + 100
        click.echo(f"{Fore.YELLOW}📊 Estimated API quota used: ~{estimated_quota} units{Style.RESET_ALL}") # I don't know that this is accurate at all, but it's a good estimate.
    
    def _format_view_count(self, count: int) -> str:
        if count >= 1_000_000:
            return f"{count / 1_000_000:.1f}M"
        elif count >= 1_000:
            return f"{count / 1_000:.1f}K"
        else:
            return str(count)


@click.command()
@click.option(
    '--query', '-q',
    help='YouTube search query (if not provided, will start interactive mode)'
)
@click.option(
    '--year', '-y',
    type=int,
    help='Year to search for videos (if not provided, will start interactive mode)'
)
@click.option(
    '--max-results', '-m',
    type=int,
    default=25,
    help='Maximum number of results to return (default: 25)'
)
@click.option(
    '--interactive', '-i',
    is_flag=True,
    default=False,
    help='Start in interactive mode for multiple searches'
)
@click.option(
    '--update-api-key', '--api-key',
    is_flag=True,
    default=False,
    help='Update your YouTube API key and exit'
)
def search(query: str, year: int, max_results: int, update_api_key: bool):
    try:
        if update_api_key:
            try:
                click.echo(f"\n{Fore.GREEN}✅ API key updated successfully!{Style.RESET_ALL}")
                click.echo(f"{Fore.BLUE}You can now use ytflashback-cli normally.{Style.RESET_ALL}")
            except (KeyboardInterrupt, click.Abort):
                click.echo(f"\n{Fore.YELLOW}API key update cancelled.{Style.RESET_ALL}")
            return
        
        cli = YouTubeSearchCLI()
        
        if query and year:
            if not cli._validate_inputs(year, max_results):
                return
            cli.search_and_display(query, year, max_results)
            
            if click.confirm(f"\n{Fore.GREEN}Would you like to search again?{Style.RESET_ALL}"):
                cli.interactive_mode()
        else:
            cli.interactive_mode()
            
    except click.Abort:
        pass


@click.command()
def update_api_key():
    """Update your YouTube API key configuration."""
    try:
        click.echo(f"{Fore.CYAN}🔑 YouTube API Key Update{Style.RESET_ALL}")
        api_key = setup_api_key_interactive()
        click.echo(f"\n{Fore.GREEN}✅ API key updated successfully!{Style.RESET_ALL}")
        click.echo(f"{Fore.BLUE}You can now use ytflashback commands normally.{Style.RESET_ALL}")
    except (KeyboardInterrupt, click.Abort):
        click.echo(f"\n{Fore.YELLOW}API key update cancelled.{Style.RESET_ALL}")
    except Exception as e:
        click.echo(f"\n{Fore.RED}Error updating API key: {e}{Style.RESET_ALL}")


if __name__ == '__main__':
    search() 
