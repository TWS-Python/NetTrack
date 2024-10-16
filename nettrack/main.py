from nettrack.gui import NetTrackGUI

def main():
    """Entry point for the NetTrack application."""
    app = NetTrackGUI()
    app.run()

if __name__ == "__main__":
    main()

import pystray
from PIL import Image, ImageDraw

def create_image():
    # Create an image for the tray icon
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), fill="black")
    return image

def quit_app(icon, item):
    icon.stop()

def setup_tray_icon():
    icon_image = create_image()
    icon = pystray.Icon("nettrack", icon_image, menu=pystray.Menu(
        pystray.MenuItem("Quit", quit_app)
    ))
    icon.run()
