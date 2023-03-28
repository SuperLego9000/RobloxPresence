import rpress as rp
from time import sleep as wait
import pypresence as pyp
import configparser
import logging
logging.basicConfig(level=logging.WARNING,format="%(levelname)s:%(message)s")
logging.getLogger(rp.__name__).setLevel(logging.DEBUG)

plr=rp.Player()
app=pyp.Presence(993591340799627284)
app.connect()

config=configparser.ConfigParser()
config.read('options.ini')


while 1:
    plr.updateStats()
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
    wait(max(config.getint('general','refreshspeed',fallback=15),5))