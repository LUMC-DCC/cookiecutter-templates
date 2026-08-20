"""Desktop application entry logic for {{ cookiecutter.project_name }}.

The desktop adapter builds a small graphical interface around project service
logic. GUI code is kept separate from the view model so display text can be
tested without opening a window.
"""

import tkinter as tk

from {{ cookiecutter.project_slug }}.adapters.desktop.view_model import build_view_model


def create_window(text: str = "{{ cookiecutter.project_name }}") -> tk.Tk:
    """Create the desktop application window.

    Parameters
    ----------
    text : str, default="{{ cookiecutter.project_name }}"
        Text to process.

    Returns
    -------
    tkinter.Tk
        Configured desktop window.
    """
    # The view model prepares text for the UI. Keeping that separate avoids
    # mixing project logic with toolkit-specific widgets.
    view_model = build_view_model(text)
    root = tk.Tk()
    root.title(view_model.title)

    # Tkinter is from the Python standard library, so this starter desktop app
    # does not add an extra GUI dependency.
    frame = tk.Frame(root, padx=24, pady=24)
    frame.pack(fill="both", expand=True)

    title = tk.Label(frame, text=view_model.title, font=("TkDefaultFont", 16, "bold"))
    title.pack(anchor="w")

    message = tk.Label(frame, text=view_model.message)
    message.pack(anchor="w", pady=(12, 0))

    return root


def main() -> None:
    """Run the desktop application event loop."""
    create_window().mainloop()


if __name__ == "__main__":
    main()
