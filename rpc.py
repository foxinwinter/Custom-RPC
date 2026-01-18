#!/home/fox/.local/share/custom-rpc/venv/bin/python

import subprocess
import json
import time
from pypresence import Presence
from pypresence.types import ActivityType

#――――――――――――――――――――――――――――――――――――――――――――#

CLIENT_ID = "placeholder"
RPC = Presence(CLIENT_ID)

#――――――――――――――――――――――――――――――――――――――――――――#

# Connect to Discord RPC
MAX_RETRIES = 5
for attempt in range(1, MAX_RETRIES + 1):
    try:
        RPC.connect()
        print("Connected to Discord RPC")
        break
    except Exception as e:
        print(f"Attempt {attempt} failed to connect to Discord RPC: {e}")
        if attempt < MAX_RETRIES:
            print("Retrying in 3 seconds...")
            time.sleep(3)
        else:
            print("Failed to connect after multiple attempts. Exiting.")
            exit(1)

#――――――――――――――――――――――――――――――――――――――――――――#

EDITOR_CLASSES = ["code", "vscode", "visual studio code", "sublime_text", "atom", "pycharm"]

def get_active_app():
    try:
        output = subprocess.check_output(["hyprctl", "-j", "activewindow"], text=True)
        data = json.loads(output)
        app_class = data.get("class", "hyprland").lower()
        title = data.get("title", "").strip()

        # Replace org.vinegarhq.sober with Roblox
        if app_class == "org.vinegarhq.sober":
            return "Roblox"

        # Shows file name + editor name for editors
        if app_class in EDITOR_CLASSES and title:
            file_name = title.split(" - ")[0].strip()
            if file_name:
                return f"{app_class} ({file_name})"

        return app_class
    except:
        return "hyprland"


def get_current_song():
    try:
        status = subprocess.check_output(["playerctl", "status"], text=True).strip()
        if status.lower() != "playing":
            return "Idle", None
        song = subprocess.check_output(
            ["playerctl", "metadata", "--format", "{{ title }}"],
            text=True
        ).strip()
        url = subprocess.check_output(
            ["playerctl", "metadata", "xesam:url"],
            text=True
        ).strip()
        return (song if song else "Idle", url if url else None)
    except subprocess.CalledProcessError:
        return "Idle", None

#――――――――――――――――――――――――――――――――――――――――――――#

while True:
    active_app = get_active_app()
    current_song, song_url = get_current_song()

    details_text = f"Listening to: {current_song}" if current_song != "Idle" else "Listening to: Idle"
    details_url = song_url if current_song != "Idle" else None

#――――――――――――――――――――――――――――――――――――――――――――#

 


    try:
        RPC.update(
            state=f"Current App: {active_app}",
            details=details_text,
            details_url=details_url,
            large_image="https://media4.giphy.com/media/v1.Y2lkPTZjMDliOTUycnRkcDl2bHY1N2s2M3NwcXY1aGJhbWJqbHN4OW05OWxyYzZnNzl4bCZlcD12MV9naWZzX3NlYXJjaCZjdD1n/a6pzK009rlCak/giphy.gif",
            large_text="i like you UwU",
            large_url="https://foxinwinter.github.io/",
            small_image="default",
            activity_type=ActivityType.PLAYING,
            party_id="null",
            name="test"
        )
        print(f"Updated RPC -> App: {active_app}, Song: {current_song}, URL: {details_url}")
    except Exception as e:
        print(f"RPC update error: {e}")

    time.sleep(2)
