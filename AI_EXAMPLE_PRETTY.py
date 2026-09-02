import json
import os
import re
from dotenv import load_dotenv
from google import genai
from rich.console import Console
from rich.markdown import Markdown, TableDataElement, TextElement
from rich.panel import Panel
from rich.theme import Theme

from T212_Super import Client


# ==============================================================================
# Configuration & Styling
# ==============================================================================

# Tokyo Night inspired theme colors:
# Soft Green: #9ece6a, Forest/Dark Green: #418c57, Soft Red: #f7768e, Cyan: #7dcfff, Blue: #7aa2f7, Purple: #bb9af7, Muted: #565f89
tokyo_night_theme = Theme({
    "pos": "#9ece6a",
    "neg": "#f7768e",
    "info": "#7dcfff",
    "dim": "#565f89",
    "accent": "#bb9af7",
    "bold_blue": "bold #7aa2f7",
    "action_sell": "bold #f7768e",       # Red
    "action_hold": "bold #9ece6a",       # Light green
    "action_buy": "bold #388e3c",        # Dark green
})
console = Console(theme=tokyo_night_theme)

TOKEN_PRICE_PER_MILLION = 0.75


# ==============================================================================
# Helper Functions
# ==============================================================================

def clear_screen() -> None:
    """Clear terminal screen reliably across Windows, Mac, and Linux."""
    os.system("cls" if os.name == "nt" else "clear")
    console.clear()


def readable_json(arg) -> str:
    """Format an object or dict as formatted JSON string."""
    return json.dumps(arg, indent=3, sort_keys=False)


NUMBER_PATTERN = re.compile(
    r'(?<![A-Za-z0-9_])([+-]?)([$€£]?\d{1,3}(?:,\d{3})*(?:\.\d+)?%?)(?![A-Za-z0-9_])'
)

ACTION_PATTERN = re.compile(r'\b(BUY|HOLD|SELL)\b', re.IGNORECASE)
ACTION_STYLES = {
    "SELL": "action_sell",
    "HOLD": "action_hold",
    "BUY": "action_buy",
}


def _highlight_rich_text(text_obj) -> None:
    """Apply pos/neg and BUY/HOLD/SELL styles directly to a Rich Text object."""
    # Highlight numbers (+ / - / currencies / percentages)
    for match in NUMBER_PATTERN.finditer(text_obj.plain):
        val = match.group(0)
        if not any(c.isdigit() for c in val):
            continue
        style = "neg" if match.group(1) == "-" else "pos"
        text_obj.stylize(style, match.start(), match.end())

    # Highlight BUY / HOLD / SELL keywords
    for match in ACTION_PATTERN.finditer(text_obj.plain):
        word = match.group(1).upper()
        if word in ACTION_STYLES:
            text_obj.stylize(ACTION_STYLES[word], match.start(), match.end())


# Hook Rich Markdown elements so parsed elements get pos/neg syntax highlighting
_orig_te_on_leave = TextElement.on_leave
def _hooked_te_on_leave(self, context):
    if hasattr(self, "text"):
        _highlight_rich_text(self.text)
    _orig_te_on_leave(self, context)
TextElement.on_leave = _hooked_te_on_leave

_orig_tde_on_leave = TableDataElement.on_leave
def _hooked_tde_on_leave(self, context):
    if hasattr(self, "content"):
        _highlight_rich_text(self.content)
    _orig_tde_on_leave(self, context)
TableDataElement.on_leave = _hooked_tde_on_leave



# ==============================================================================
# Initialization & Data Fetching
# ==============================================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

t212_client = Client()
ai_client = genai.Client(api_key=GEMINI_API_KEY)

portfolio_data = readable_json(t212_client.positions.getPositions())
# portfolio_data = readable_json(t212_client.account.summary())

prompt = (
    "You are a financial advisor. Take a neutral, unbiased stance. "
    f"See my portfolio: {portfolio_data}. Based on recent movement and news of the stock, "
    "what would you advise me to do for each position and why? BUY/HOLD/SELL?"
)


# ==============================================================================
# Streaming Execution & Display
# ==============================================================================

clear_screen()
console.print("[dim]Generating advice...[/dim]\n")

stream = ai_client.interactions.create(
    model="gemini-3.8-flash",
    input=prompt,
    stream=True,
)

full_response = []
usage = None

for event in stream:
    if event.event_type == "step.delta":
        if event.delta.type == "text":
            full_response.append(event.delta.text)
            print(event.delta.text, end="", flush=True)
    elif event.event_type == "interaction.completed":
        usage = event.interaction.usage
    elif event.event_type == "step.stop" and getattr(event, "usage", None):
        usage = event.usage

full_text = "".join(full_response)
if full_text:
    clear_screen()
    console.print(Markdown(full_text))

if usage:
    cost = (usage.total_tokens / 1_000_000) * TOKEN_PRICE_PER_MILLION
    usage_summary = (
        f"[accent]Input tokens:[/accent]  {usage.total_input_tokens}\n"
        f"[accent]Output tokens:[/accent] {usage.total_output_tokens}\n"
        f"[accent]Total tokens:[/accent]  {usage.total_tokens}\n"
        f"[bold_blue]Estimated Cost:[/bold_blue] [pos]${cost:.6f}[/pos]"
    )
    console.print(
        Panel(
            usage_summary,
            title="[info]Token Usage[/info]",
            border_style="#565f89",
            expand=False,
        )
    )

# Used AI for reorganizing this code.