import rpress as rp
from time import sleep as wait
import pypresence as pyp
import configparser
import logging
logging.basicConfig(level=logging.WARNING,format="%(levelname)s:%(message)s")
logging.getLogger(rp.__name__).setLevel(logging.DEBUG)

plr=rp.Player()
app=pyp.Presence(993591340799627284)

config=configparser.ConfigParser()
config.read('options.ini')

connected:bool=False
while 1:
    plr.updateStats()
    if connected and plr.state==0:
        print("Stopped playing roblox")
        app.close()
        connected=False
    elif not connected and not plr.state==0:
        print("Started playing roblox")
        app.connect()
        connected=True
    
    if not connected:
        print("waiting for activity...")
    if connected and not plr.state==0:
        buttons=[{'label':"Profile Page",'url':rp.Endpoints.userPage%plr.id}] if config.getboolean('display','showprofile',fallback=True) else []
        if plr.state in [2,3] and config.getboolean('display','showgame',fallback=True):buttons.append({'label':"Game Page","url":plr.gamePath})
        app.update(
            details='%s %s'%(rp.Enums.playingState[plr.state],plr.gameName if config.getboolean('display','showgame',fallback=True) else 'a game' if plr.state in [2,3] else ''),
            large_image=plr.iconPath if config.getboolean('display','showgame',fallback=True) else rp.Endpoints.defaultIcon,
            large_text='%s on Roblox'%plr.gameName if plr.state in [2,3] and config.getboolean('display','showgame',fallback=True) else 'Roblox',
            buttons=buttons if len(buttons)>=1 else None,
            small_image=rp.Enums.playingIcon[plr.state] if config.getboolean('display','showicon',fallback=False) else None,
            start=plr.timestamp if plr.state in [2,3] and config.getboolean('display','showtime',fallback=True) else None
        )
    lastState=plr.state
    wait(max(config.getint('general','refreshspeed',fallback=15),5))