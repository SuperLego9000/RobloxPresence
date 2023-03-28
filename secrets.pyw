import base64
from time import sleep as wait

def cookie():
    cookie=''
    try:
        with open('secrets.txt','r') as f:
            cookie=f.readlines()[0]
        return {'.ROBLOSECURITY':base64.b64decode(cookie).decode('ascii')}
    except FileNotFoundError:
        print("secrets.txt not found.\nplease login.")
        print("Ctrl+C to exit...")
        try:wait(9e9)
        except KeyboardInterrupt:pass
        exit(1)
