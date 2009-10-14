import urllib
import urllib2
import re

from urllib2 import URLError, HTTPError

error = None
wave = None
auth = None

errorPattern = 'Error=([A-z]+)'
authPattern = 'Auth=([A-z0-9_-]+)'
wavePattern = 'SID=([A-z0-9_-]+)'

def login(username, password):
    parameters = {'accountType': 'GOOGLE',
                  'Email': username,
                  'Passwd': password,
                  'service': 'wave',
                  'source': 'wave-check-o-rama-0.0.1'}

    request = urllib2.Request('https://www.google.com/accounts/ClientLogin')
    data = urllib.urlencode(parameters)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')

    try:
        response = urllib2.urlopen(request, data)
        parseLogin(response)
        response.close()
    except HTTPError, error:
        print error
    except URLError, error:
        print error

def parseLogin(response):
    global auth
    global wave

    responseText = response.read()

    error = re.search(errorPattern, responseText)
    auth = re.search(authPattern, responseText).group(1)
    wave = re.search(wavePattern, responseText).group(1)

    if error:
        print 'Error occurred while logging in'
    else:
        if auth and wave:
            readInbox() 

def readInbox():

    inboxURL = 'https://wave.google.com/wave/?nouacheck'
    parameters = {'auth': urllib.quote(auth)}

    data = urllib.urlencode(parameters)
    request = urllib2.Request(inboxURL, data)
    request.add_header('WAVE', urllib.quote(wave))

    try:
        response = urllib2.urlopen(request)
        parseInbox(response)
        response.close()
    except HTTPError, error:
        print error
    except URLError, error:
        print error

def parseInbox(response):
    responseText = response.read()
    
    data = re.search('var json = (\{"r":"\^d1".*});', responseText)
    data = re.findall('"7":([0-9]+),', data.group(1))

    messages = 0
    unread = 0

    for wavelet in data:
        messages += 1
        unread += int(wavelet)

    print 'Unread: %s' % (unread)
    print 'Messages: %s' % (messages)

if __name__ == '__main__':
    login()
