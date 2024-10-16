import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from nettrack.utils import get_network_stats, get_ip_address, get_interface_stats


class NetTrackGUI:
    def __init__(self):
        """Initialize the Tkinter window."""
        self.root = tk.Tk()
        self.root.title("NetTrack - Network Monitoring")
        self.root.geometry("800x600")

        # Theme toggle variable
        self.is_dark_mode = tk.BooleanVar(value=False)  # Default to light mode

        # Set up the initial theme (light mode)
        self.setup_theme()

        # Set up the GUI components
        self.setup_ui()

    def setup_theme(self):
        """Set the theme based on the mode (light/dark)."""
        if self.is_dark_mode.get():
            # Dark theme settings
            self.root.configure(bg="#2e2e2e")
            self.style = ttk.Style(self.root)
            self.style.configure('TButton', font=('Helvetica', 12), padding=6, background='#444444', foreground='black')
            self.style.configure('TLabel', font=('Helvetica', 12), background='#2e2e2e', foreground='white', padding=4)
            self.stats_display_style = {"bg": "#1c1c1c", "fg": "#ffffff", "insertbackground": "white",
                                        "state": "disabled"}
        else:
            # Light theme settings
            self.root.configure(bg="#f0f0f0")
            self.style = ttk.Style(self.root)
            self.style.configure('TButton', font=('Helvetica', 12), padding=6, background='#e0e0e0', foreground='black')
            self.style.configure('TLabel', font=('Helvetica', 12), background='#f0f0f0', foreground='black', padding=4)
            self.stats_display_style = {"bg": "#ffffff", "fg": "#000000", "insertbackground": "black",
                                        "state": "disabled"}

    def setup_ui(self):
        """Set up the UI components with a responsive layout."""

        # Configure grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)  # For the stats display

        # Title label
        title_label = ttk.Label(self.root, text="NetTrack", font=("Helvetica", 20))
        title_label.grid(row=0, column=0, pady=10, sticky='n')

        # ScrolledText for displaying network stats (non-editable)
        self.stats_display = scrolledtext.ScrolledText(self.root, font=("Arial", 10), **self.stats_display_style)
        self.stats_display.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.stats_display.config(state='disabled')  # Set to non-editable initially

        # Button frame
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=2, column=0, pady=5, padx=10, sticky='ew')
        button_frame.config(style="TFrame")

        # Configure button frame grid
        button_frame.columnconfigure([0, 1], weight=1)

        # Refresh button with consistent text color
        self.refresh_button = ttk.Button(button_frame, text="Refresh Stats", command=self.update_stats)
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        # Quit button with consistent text color
        self.quit_button = ttk.Button(button_frame, text="Quit", command=self.root.quit)
        self.quit_button.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Status bar using ttk
        self.status_label = ttk.Label(self.root, text="Status: Ready", anchor=tk.W)
        self.status_label.grid(row=3, column=0, sticky='ew', padx=10, pady=(0, 5))

        # Dark Theme Toggle (Checkbox with label)
        theme_frame = ttk.Frame(self.root)
        theme_frame.grid(row=4, column=0, pady=5, padx=10, sticky='e')
        self.theme_checkbox = ttk.Checkbutton(theme_frame, text="Dark Theme", variable=self.is_dark_mode,
                                              command=self.toggle_theme)
        self.theme_checkbox.pack(side=tk.RIGHT)

        # Show initial stats
        self.update_stats()

    def toggle_theme(self):
        """Toggle between dark and light modes based on the checkbox state."""
        self.setup_theme()  # Re-apply the theme
        self.update_ui_appearance()  # Update the UI with the new theme

    def update_ui_appearance(self):
        """Update the UI components' appearance according to the selected theme."""
        # Update background and text color for the scrolled text display
        self.stats_display.configure(**self.stats_display_style)

        # Refresh the displayed stats to apply the theme
        self.update_stats()

    def update_stats(self):
        """Update the network statistics displayed."""
        self.status_label.config(text="Status: Updating...")
        stats = get_network_stats()
        ip_address = get_ip_address()
        interfaces = get_interface_stats()

        # Allow writing to the stats display before disabling again
        self.stats_display.config(state='normal')
        self.stats_display.delete(1.0, tk.END)
        self.stats_display.insert(tk.INSERT, f"IP Address: {ip_address}\n\n")
        self.stats_display.insert(tk.INSERT, f"Network Interfaces:\n{interfaces}\n\n")
        self.stats_display.insert(tk.INSERT, f"Network Stats:\n{stats}\n")
        self.stats_display.config(state='disabled')  # Set back to non-editable

        self.status_label.config(text="Status: Updated")

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()
