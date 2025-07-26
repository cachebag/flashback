from textual.app import ComposeResult
from textual.containers import Center, Middle, Vertical
from textual.widgets import Input, Button, Label, Static, Footer
from textual.screen import Screen, ModalScreen
from textual.validation import ValidationResult, Validator

from ..utils import save_api_key


class APIKeyValidator(Validator):
    
    def validate(self, value: str) -> ValidationResult:
        if not value.strip():
            return self.failure("API key cannot be empty")
        
        if len(value.strip()) < 20:
            return self.failure("API key seems too short")
        
        return self.success()


class SetupScreen(Screen):
    
    BINDINGS = [
        ("ctrl+q", "quit", "Quit"),
        ("escape", "quit", "Quit"),
    ]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = None
    
    def compose(self) -> ComposeResult:
        yield Center(
            Middle(
                Vertical(
                    Static("🔑 YouTube API Key Setup", id="title"),
                    Static("", id="spacer1"),
                    Static("You need a YouTube Data API v3 key to use this application.", id="description"),
                    Static("", id="spacer2"),
                    Static("To get your free API key:", id="instructions_title"),
                    Static("1. Go to https://console.cloud.google.com/", id="step1"),
                    Static("2. Create a new project or select existing one", id="step2"),
                    Static("3. Enable the YouTube Data API v3", id="step3"),
                    Static("4. Create credentials (API key)", id="step4"),
                    Static("5. Copy your API key and paste it below", id="step5"),
                    Static("", id="spacer3"),
                    Input(
                        placeholder="Enter your YouTube API key...",
                        password=True,
                        validators=[APIKeyValidator()],
                        id="api_key_input"
                    ),
                    Static("", id="spacer4"),
                    Button("Save API Key", variant="primary", id="save_button"),
                    Button("Quit", variant="default", id="quit_button"),
                    Label("", id="status"),
                    id="setup_form"
                )
            )
        )
        yield Footer()
    
    def on_mount(self) -> None:
        self.query_one("#api_key_input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "save_button":
            self.save_api_key()
        elif event.button.id == "quit_button":
            self.app.exit()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "api_key_input":
            self.save_api_key()
    
    def save_api_key(self) -> None:
        api_key_input = self.query_one("#api_key_input", Input)
        status_label = self.query_one("#status", Label)
        
        api_key = api_key_input.value.strip()
        
        if not api_key:
            status_label.update("❌ Please enter an API key")
            return
        
        if len(api_key) < 20:
            status_label.update("❌ API key seems too short. Please check and try again.")
            return
        
        try:
            save_api_key(api_key)
            status_label.update("✅ API key saved successfully!")
            self.api_key = api_key
            
            self.set_timer(1.0, self.continue_to_app)
            
        except ValueError as e:
            status_label.update(f"❌ Error saving API key: {e}")
    
    def continue_to_app(self) -> None:
        self.dismiss(self.api_key)


class SetupModal(ModalScreen):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = None
    
    def compose(self) -> ComposeResult:
        yield Center(
            Middle(
                Vertical(
                    Static("🔑 Update YouTube API Key", id="modal_title"),
                    Static("", id="modal_spacer1"),
                    Input(
                        placeholder="Enter your new YouTube API key...",
                        password=True,
                        validators=[APIKeyValidator()],
                        id="modal_api_key_input"
                    ),
                    Static("", id="modal_spacer2"),
                    Button("Save", variant="primary", id="modal_save_button"),
                    Button("Cancel", variant="default", id="modal_cancel_button"),
                    Label("", id="modal_status"),
                    id="modal_setup_form"
                )
            )
        )
    
    def on_mount(self) -> None:
        self.query_one("#modal_api_key_input", Input).focus()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "modal_save_button":
            self.save_api_key()
        elif event.button.id == "modal_cancel_button":
            self.dismiss(None)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "modal_api_key_input":
            self.save_api_key()
    
    def save_api_key(self) -> None: 
        api_key_input = self.query_one("#modal_api_key_input", Input)
        status_label = self.query_one("#modal_status", Label)
        
        api_key = api_key_input.value.strip()
        
        if not api_key:
            status_label.update("❌ Please enter an API key")
            return
        
        if len(api_key) < 20:
            status_label.update("❌ API key seems too short. Please check and try again.")
            return
        
        try:
            save_api_key(api_key)
            status_label.update("✅ API key saved successfully!")
            self.api_key = api_key
            
            self.set_timer(1.0, self.dismiss_with_result)
            
        except ValueError as e:
            status_label.update(f"❌ Error saving API key: {e}")
    
    def dismiss_with_result(self) -> None:
        self.dismiss(self.api_key) 