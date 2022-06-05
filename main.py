from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import base64
import random
import string
import json
import cloudscraper

APP_KEY = "7B5D7BC24B5C4E3A80FBBC2A1156E437" # Found in cource code

session = cloudscraper.create_scraper(
    ## Credit @VeNoMouSNZ 
    browser={
        'browser': 'firefox',
        'platform': 'android',
        'mobile': True
    }
)


def generateIV(N):
  
    ## Can use os.urandom(N) too 
    
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    arrayList = []
    for i in range(N):
        arrayList.append(random.choice(chars))
    joinToString = ''.join(arrayList)
    charset  = "UTF-8"

    if joinToString != None:
        arrayListBytes = bytes(joinToString, charset)
        return arrayListBytes

def encryptToken(token):
    charset = "UTF-8"
    iv = generateIV(16)
    cipher = Cipher(algorithms.AES(bytes(APP_KEY, charset)), modes.CBC(iv))
    padder = padding.PKCS7(128).padder()
    encryptor = cipher.encryptor()

    if token != None:
        tokenBytes = bytes(token, charset)
        added_data = padder.update(tokenBytes)
        added_data += padder.finalize()
        doFinal = encryptor.update(added_data) + encryptor.finalize()
        encodeToString = base64.b64encode(doFinal).decode('utf-8')

        if encodeToString != None:
            sb = iv.decode('utf-8') + encodeToString
            return sb

headers = {
    'accept-encoding': 'gzip',
    'connection': 'Keep-Alive',
    'content-type': 'application/x-www-form-urlencoded',
    'host': 'api-e3.nuqlium.com',
    'user-agent': 'okhttp/4.6.0'
}

payload = 'username=footasylum-b12cf60a-0db8-40a1-aaf6-04e6ffe4e342&password=553c3198-652a-4355-97b9-d6b0e5a6e15d&grant_type=password'

res = session.post('https://api-e3.nuqlium.com/api/token', headers=headers, data=payload)

jsondata = json.loads(res.text)

bearer = jsondata['access_token']
token = jsondata['oauth-verification-token']

oauthToken = encryptToken(token)

## Now you have your encrypted token, you can make the requests that need this token
