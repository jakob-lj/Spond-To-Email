import os
import requests
import datetime
from dotenv import load_dotenv
load_dotenv()

def sendEmail(teamName, going):
    pass

def getPerson(event, id):
    member = list(filter(lambda x: x['id'] == id, event['recipients']['groups'][0]['members']))[0]

    return member['lastName'] + ", " + member['firstName'] + " (tlf på forespørsel)"
    #return event['recipients']['groups'][0]['members']
    #return "jakob"

def send(event):
    if (event):
        teamName = event['recipients']['groups'][0]['name']
        going = []
        for member in event['responses']['acceptedIds']:
            person = getPerson(event, member)
            going.append(person)
        sendEmail(teamName, going)
    else:
        print("pass")
        pass

def load():
    baseUrl = os.environ['spondsBaseUrl'] % (os.environ['groupId'], str(datetime.datetime.now()).replace(" ", "T") + "Z")

    cookies = {'auth':os.environ['accessToken']}
    result = requests.get(baseUrl, cookies=cookies)
    data = result.json()
    eventToBeSent = None

    for spond in data:

        time = datetime.datetime.strptime(spond['startTimestamp'], "%Y-%m-%dT%H:%M:%SZ")
        diff = time - datetime.datetime.now()
        if (diff.days == 1):
            eventToBeSent = spond
            break
        
    send(eventToBeSent)
load()