import os
import requests
import datetime
from dotenv import load_dotenv

load_dotenv()

def log(text):
    print(text)
    with open('log.txt', 'a') as f:
        f.write("%s: " % datetime.datetime.now() + str(text) + "\n")

def sendEmail(teamName, going):
    mems = ""
    for n in going:
        mems = mems + "%s\n" % n
    #print(mems)
    
def getEventName(event):
    return event['heading']

def getPerson(event, id):
    member = list(filter(lambda x: x['id'] == id, event['recipients']['groups'][0]['members']))[0]
    
    if ('lastName' in member.keys()):
        return str(member['lastName']) + ", " + str(member['firstName']) + " (tlf på forespørsel)"
    elif ('firstName' in member.keys()):
        return member['firstName']
    else:
        return 'Navnløst medlem'
    
def getTeamName(event):
    teamName = event['recipients']['groups'][0]['name']
    return teamName

def send(event):
    teamName = getTeamName(event)
    going = []
    for member in event['responses']['acceptedIds']:
        person = getPerson(event, member)
        going.append(person)
    sendEmail(teamName, going)


def load():
    baseUrl = os.environ['spondsBaseUrl'] % (str(datetime.datetime.now()-datetime.timedelta(days=0.25)).replace(" ", "T") + "Z")
    cookies = {'auth':os.environ['accessToken']}
    result = requests.get(baseUrl, cookies=cookies)
    data = result.json()
    

    for spond in data:
        time = datetime.datetime.strptime(spond['startTimestamp'], "%Y-%m-%dT%H:%M:%SZ")
        diff = time - datetime.datetime.now()
        if (diff.days == 1):
            log("Sending spond for group: %s" % getTeamName(spond))
            #log(spond)
            send(spond)
            

load()