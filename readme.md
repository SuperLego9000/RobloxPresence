# Roblox Presence
## About
simple Discord rpc written in Python for more detailed 'Playing' section
## Notes
The Roblox api requires a user token to get game details even if the account's joins are set to everyone.
Roblox Presence **will not upload your token and it will not leave this device unless it is being used for the Roblox api!**

**If you are uncomfortable with accessing your token this app is not for you**, you may look through the [source code](https://github.com/SuperLego9000/RobloxPresence/blob/main/rpress.py) on the github and analyze network traffic if you desire.
# Install
Install the latest release of Roblox Presence [here](https://github.com/SuperLego9000/RobloxPresence/releases)
### Accessing your token
 - navigate to [Roblox](https://www.roblox.com/home)
 - open the Inspector ctrl+shift+i
 - goto the `Application` tab at the top
 - on the right under `Storage` expand `Cookies`
 - click `https://www.roblox.com`
 - copy the `Value` from the `Name` "`.ROBLOSECURITY`"
### Loading your account
- after you download and extract Roblox Presence open the file named `RobloxPresence-Login`
- **paste your token** into the prompt and press enter
**it will then encrypt your token for safety** and store it in `secrets.txt`
### Starting the program
after you have stored your token you can run `RobloxPresence.exe` or see [Config](#Config) for customization options
# Config
Roblox Presence allows for a file in the same directory named `options.ini` to control certain features
here is an example of what that file may look like
```ini options.ini
[general]
refreshspeed=15 ; how often to ask roblox what your account is playing (minimum 5 seconds)
[display]
showgame=true ; game image, name, and button
showprofile=true ; profile button
showtime=true ; time playing
showicon=false
```