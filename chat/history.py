import json
import os

def readHistory(username):
    username1 = username.split(' - ')
    username1.reverse()
    username1 = '{} - {}'.format(username1[0], username1[1])
    username2 = username
    url1 = 'media/user/history/{}.json'.format(username1)
    url2 = 'media/user/history/{}.json'.format(username2)
    
    data = {
        
    }
    
    if len(username.split(' - ')) != 2:
        return "ignore username"
    
    if os.path.exists(url1):
        with open(url1) as history:
            data = json.load(history) 
    elif os.path.exists(url2):
        with open(url2) as history:
            data = json.load(history)
    else:
        return "file not found"
    
    return data

def writeHistory(username):
    pass