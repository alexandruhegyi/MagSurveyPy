"""Cross-platform terminal banner for MagSurveyPy.

The banner is kept separate from the scientific processing engine so terminal
branding cannot affect processing logic.  It uses UTF-8 box/Braille characters
when the terminal supports them and adds theme-neutral ANSI styling only after
padding each line, so escape sequences never move the right border.
"""
from __future__ import annotations

import os
import sys

RESET = "\x1b[0m"
DIM_DEFAULT = "\x1b[2;39m"
DEFAULT_FG = "\x1b[39m"
BOLD_DEFAULT = "\x1b[1;39m"

INNER_WIDTH = 77


def _enable_utf8_and_vt() -> bool:
    """Best-effort UTF-8 + ANSI support on Linux/macOS/Windows.

    Returns True when colour should be emitted.  Plain UTF-8 is still printed
    when colour is disabled (e.g. redirected output or NO_COLOR).
    """
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    if os.name == "nt":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleOutputCP(65001)
            STD_OUTPUT_HANDLE = -11
            ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
            handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
            mode = ctypes.c_uint32()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                kernel32.SetConsoleMode(handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        except Exception:
            pass

    if os.environ.get("NO_COLOR"):
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    try:
        return bool(sys.stdout.isatty())
    except Exception:
        return False


def _fit(text: str) -> str:
    # The characters used here render as one terminal column on modern UTF-8
    # terminals.  Padding occurs before ANSI styling is inserted.
    return text[:INNER_WIDTH].ljust(INNER_WIDTH)


def _box_line(text: str, colour: bool, spans=()) -> str:
    plain = _fit(text)
    if not colour:
        return f"│{plain}│"
    # Apply colour to spans after padding, preserving visible width exactly.
    pieces = []
    pos = 0
    for start, end, code in sorted(spans, key=lambda x: x[0]):
        start = max(0, min(INNER_WIDTH, start))
        end = max(start, min(INNER_WIDTH, end))
        if start > pos:
            pieces.append(plain[pos:start])
        pieces.append(code + plain[start:end] + RESET)
        pos = end
    if pos < INNER_WIDTH:
        pieces.append(plain[pos:])
    return DIM_DEFAULT + "│" + RESET + "".join(pieces) + DIM_DEFAULT + "│" + RESET


def banner_text(version: str = "1.0.3", author: str = "Alexandru Hegyi, PhD",
                website: str = "https://alexandruhegyi.com",
                email: str = "alexandruhegyi@gmail.com", colour: bool = False) -> str:
    mesh = [
        "   ⢀⣀⣤⣤⣤⣤⣤⣀⡀",
        "   ⢻⣿⣿⠟⠉⠙⢿⣿⣿",
        "   ⣸⣿⣿  █  ⣸⣿⣿",
        "   ⢹⣿⣿⣀⣀⣀⣸⣿⣿",
        "   ⠈⠉⠛⠛⠛⠛⠉⠉",
    ]
    right = [
        "",
        f"MagSurveyPy v{version}",
        "───────────────────────────────────────────────────",
        "Archaeological Magnetometry Prospection Suite",
        f"Developed by {author}",
    ]
    lines = []
    top = "┌" + "─" * INNER_WIDTH + "┐"
    bottom = "└" + "─" * INNER_WIDTH + "┘"
    lines.append((DIM_DEFAULT + top + RESET) if colour else top)

    # Compact two-column composition.  Right column starts at character 24.
    for i in range(5):
        base = _fit(mesh[i])
        chars = list(base)
        r = right[i]
        start = 24
        for j, ch in enumerate(r[:INNER_WIDTH-start]):
            chars[start+j] = ch
        text = "".join(chars)
        spans = [(3, min(21, len(text)), DEFAULT_FG)]
        if i == 1:
            spans.append((24, min(24+len(r), INNER_WIDTH), BOLD_DEFAULT))
        elif i in (2,3,4):
            spans.append((24, min(24+len(r), INNER_WIDTH), DEFAULT_FG))
        lines.append(_box_line(text, colour, spans))

    contact = f"{website} | {email}"
    cstart = max(2, INNER_WIDTH - len(contact) - 1)
    contact_line = " " * cstart + contact
    lines.append(_box_line(contact_line, colour,
                           [(cstart, min(cstart+len(contact), INNER_WIDTH), DEFAULT_FG)]))
    lines.append((DIM_DEFAULT + bottom + RESET) if colour else bottom)
    return "\n".join(lines)


def print_banner(version: str = "1.0.3", author: str = "Alexandru Hegyi, PhD",
                 website: str = "https://alexandruhegyi.com",
                 email: str = "alexandruhegyi@gmail.com") -> None:
    colour = _enable_utf8_and_vt()
    print(banner_text(version, author, website, email, colour=colour), flush=True)


if __name__ == "__main__":
    print_banner()
