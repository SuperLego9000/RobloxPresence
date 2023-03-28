import base64
from time import sleep as wait

token=input('token: ')
with open('secrets.txt','w') as f:
    f.write(
        base64.b64encode(token.encode('ascii')).decode('ascii')
    )
    print('hashed token into secrets file.')
    print('exiting...')
    wait(3)