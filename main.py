import os
from pynput import keyboard
import threading
from time import sleep
import app.Spotify_custom as s
from app.utils import *







CONFIG={}

def updateConfig():
	global CONFIG
	CONFIG_PATH=os.path.abspath("./config.yaml")
	CONFIG=loadConfig(CONFIG_PATH)
updateConfig()

from dotenv import load_dotenv
load_dotenv()

pause = False
SPOTIFY = s.Spotify_custom()


def close():
	print(f"BYE!\n{line()}")
	SPOTIFY.exit()
	sleep(2)
	exit()

SHORTCUTS={}

def populateShortcuts(name,command,multiple=False):
	global SHORTCUTS
	if not name in CONFIG: return None
	data = CONFIG[name]
	if not data: return None
	if multiple and (type(data) is not dict): return None
	if not multiple and (type(data) is not str): return None

	if not multiple:
		SHORTCUTS[data]=[command,None]
		return
	

	for key,value in data.items():
		if not value or type(value) is not str: continue
		SHORTCUTS[key.lower()]=[command,value]
	

def updateShortcuts():
	global SHORTCUTS
	updateConfig()
	SHORTCUTS={}
	populateShortcuts(ADD_TO_PLAYLIST,SPOTIFY.add_current_to_playlist,True)
	populateShortcuts(REM_FR_PLAYLIST,SPOTIFY.remove_current_from_playlist,True)
	
	populateShortcuts(ADD_TO_LIKED,SPOTIFY.add_current_to_liked)
	populateShortcuts(REM_FR_LIKED,SPOTIFY.remove_current_from_liked)
	
	populateShortcuts(TGL_LOOP,SPOTIFY.loop_toggle)
	populateShortcuts(TGL_SHUFFLE,SPOTIFY.shuffle_toggle)
	
	populateShortcuts(CLOSE,close)
	populateShortcuts(PAUSE,None)

	populateShortcuts(UPD_SHORTCUTS,updateShortcuts)
	
	print(f"UPDATED SHORTCUTS\n{line()}")

	
updateShortcuts()

def press(key):
	global pause
	if not SHORTCUTS:
		updateShortcuts()


	k = key.char if hasattr(key,'char') else key.name if hasattr(key,'name') else key

	if k == CONFIG[PAUSE]:
			pause = not pause
			if not pause:
					print(f"RESUMED\n{line()}")
			else:
				print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
			return

	if pause and k in SHORTCUTS.keys():
			print(f"PAUSED -> press [{CONFIG[PAUSE]}] to resume\n{line()}")
			return

	if pause:
			return

	if k not in SHORTCUTS:
			return

	if SHORTCUTS[k][1]:
			SHORTCUTS[k][0](SHORTCUTS[k][1])
	else:
			SHORTCUTS[k][0]()







def listener():
	with keyboard.Listener(on_press=press) as listener:
			listener.join()


th1 = threading.Thread(target=listener, name="LISTENER").start()
