import tkinter as tk
from tkinter import messagebox
from nettrack.utils import get_network_stats

class NetTrackGUI:
    def __init__(self):
        """Initialize the Tkinter window."""
        self.root = tk.Tk()
        self.root.title("NetTrack - Network Monitoring")
        self.root.geometry("400x300")

        # Set up the GUI components
        self.setup_ui()

    def setup_ui(self):
        """Set up the UI components."""
        label = tk.Label(self.root, text="NetTrack", font=("Helvetica", 16))
        label.pack(pady=10)

        self.stats_button = tk.Button(self.root, text="Get Network Stats", command=self.show_stats)
        self.stats_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quit", command=self.root.quit)
        self.quit_button.pack(pady=10)

    def show_stats(self):
        """Display the network statistics."""
        stats = get_network_stats()
        messagebox.showinfo("Network Stats", stats)

    def run(self):
        """Run the Tkinter main loop."""
        self.root.mainloop()
