import base64

def cookie():
    cookie=''
    with open('secrets.txt','r') as f:
        cookie=f.readlines()[0]
    return {'.ROBLOSECURITY':base64.b64decode(cookie).decode('ascii')}