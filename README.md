# send-key-test

A macOS TUI tool that automatically sends CMD+Tab at a configurable interval using AppleScript.

## Usage

```bash
python3 send_cmd_tab.py
```

## Controls

| Key | Action |
|---|---|
| `Space` | Pause / Resume |
| `Up` / `+` | Increase interval by 0.5s |
| `Down` / `-` | Decrease interval by 0.5s |
| `r` | Reset counter |
| `q` | Quit |

## Requirements

- macOS (uses `osascript` and System Events)
- Python 3
- Accessibility permissions for your terminal app
