class Endpoints:
    groupIcon='https://thumbnails.roblox.com/v1/groups/icons?groupIds=%s&size=150x150&format=Png&isCircular=false'
    userStatus='https://presence.roblox.com/v1/presence/users'
    gameInfo='https://games.roblox.com/v1/games/multiget-place-details?placeIds=%s'
    universeIcon='https://thumbnails.roblox.com/v1/games/icons?universeIds=%s&returnPolicy=PlaceHolder&size=512x512&format=Png&isCircular=false'
    authedUser='https://users.roblox.com/v1/users/authenticated'
    gamePage='https://www.roblox.com/games/%s/'
    userPage='https://www.roblox.com/users/%s/profile'
    defaultIcon='https://tr.rbxcdn.com/4fb7366e93a007b582ba3f5a5df1168d/150/150/Image/Png'
class Enums:
    gameState=['offline','online','ingame','studio']
    playingState=['Offline','Online','Playing','In Studio:']
    playingIcon=[None,'blue','green','orange']
import json
import requests
import datetime
import secrets

import logging
logger = logging.getLogger(__name__)

class Player:
    id:int=0
    '''playerId'''
    state:int=0
    '''OnlineEnum'''
    gameId:int=0
    gameName:str=''
    iconPath:str=''
    '''hyperlink to game thumbnail'''
    gamePath:str=''
    '''hyperlink to frontend gamepage'''
    timestamp:int=0
    '''since started playing'''

    def __init__(self,id:int=None):
        if id==None or not isinstance(id,int):
            req=requests.get(Endpoints.authedUser,headers={'accept':"application/json"},cookies=secrets.cookie())
            if req.status_code!=200:
                raise ValueError("failed to get account from cookie.")
            id=json.loads(req.content)['id']
            logger.info(f'found user "{json.loads(req.content)["name"]}" in cookie')
        self.id=id
    
    def updateStats(self):
        old=self.gameId
        self.updateGame()
        if not self.gameId == old:
            self.updateIcon()
        logger.info("status updated sucessfully.")
    def updateGame(self):
        logger.info("requesting game info...")
        req=requests.post(Endpoints.userStatus,data='{"userIds": [%d]}'%self.id,headers={'content-type':"text/json",'accept':"application/json"},cookies=secrets.cookie())
        raw=json.loads(req.content)
        res=raw['userPresences'][0]
        self.state=res['userPresenceType']
        old=self.gameId
        logger.debug('user '+Enums.gameState[res['userPresenceType']])
        match res['userPresenceType']:
            case 2|3:
                logger.debug("user playing/creating game")
                self.gameId=res['universeId']
                self.gameName=res['lastLocation']
                self.gamePath=Endpoints.gamePage%res['rootPlaceId']
            case _:
                logger.debug("user inactive")
                self.gameId=-1
                self.gameName=''
                self.gamePath=''
        if not self.gameId==old:
            logger.debug("timestamp changed.")
            self.timestamp=int(datetime.datetime.fromisoformat(res['lastOnline']).timestamp())
        logger.info("game updated.")

    def updateIcon(self):
        logger.info('finding icon...')
        req=requests.get(Endpoints.universeIcon%self.gameId,cookies=secrets.cookie())
        lnk=''
        try:
            if not req.status_code==200:raise BaseException
            #if not json.loads(req.content)['data'][0]['state']=='completed':raise BaseException

            lnk=json.loads(req.content)['data'][0]['imageUrl']
            logger.debug('found icon.')
        except BaseException as e:
            logger.warning('failed to find game icon. using default.')
            lnk=Endpoints.defaultIcon
        finally:
            logger.info("applying icon...")
            self.iconPath=lnk
