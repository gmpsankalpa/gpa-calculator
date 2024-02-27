# themes.py

THEMES = {
    "light": {
        "bg": "white",
        "fg": "black",
        "button_bg": "#eeeeee",  # Light gray
        "button_fg": "black",
    },
    "dark": {
        "bg": "#2d2d2d",  # Dark gray
        "fg": "white",
        "button_bg": "#555555",  # Darker gray
        "button_fg": "white",
    },
}

def apply_theme(root, theme):
    selected_theme = THEMES.get(theme, THEMES["light"])  # Default to light theme if theme not found
    root.configure(bg=selected_theme["bg"])

    for widget in root.winfo_children():
        apply_widget_theme(widget, selected_theme)


def apply_widget_theme(widget, theme):
    if widget.winfo_class() == "Button":
        widget.configure(bg=theme["button_bg"], fg=theme["button_fg"])
    else:
        widget.configure(bg=theme["bg"], fg=theme["fg"])
