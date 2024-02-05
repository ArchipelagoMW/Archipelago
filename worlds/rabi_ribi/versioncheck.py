import requests
import json
from utility import print_ln

VERSION_STRING = '{PLACEHOLDER_VERSION}'

def get_current_branch():
    if '#' in VERSION_STRING: return VERSION_STRING.split('#')[1][:1]
    return 'D'

def fetch_latest_version_id():
    PREFIX = 'https://ci.appveyor.com/api/'
    ERROR_UPDATING = 'Either the Randomizer is currently being updated on AppVeyor, or some other strange error has occurred.'
    ERROR_UNKNOWN = 'Unknown error retrieving latest version number.'
    try:
        req = requests.get(PREFIX + 'projects/wcko87/rabiribi-randomizer-ui-rc94b')
        jobs = json.loads(req.text)['build']['jobs']
        if len(jobs) == 0:
            return False, ERROR_UPDATING
        jobid = jobs[0]['jobId']

        req = requests.get(PREFIX + 'buildjobs/%s/messages' % jobid)
        messages = json.loads(req.text)['list']
        messages = [d['message'] for d in messages]

        branch = get_current_branch()
        for message in messages:
            if message.startswith(branch):
                return True, message[message.find(':')+1:].lstrip()
        return False, ERROR_UPDATING
    except:
        return False, ERROR_UNKNOWN
    
def check_branch():
    print_ln(get_current_branch())

def check_for_updates():
    result, message = fetch_latest_version_id()
    if result:
        if VERSION_STRING == message: result = 'You have the latest version of Randomizer.'
        else: result = 'Randomizer version does not match latest version.'
        sb = [
            result,
            '',
            'Current Version: %s' % VERSION_STRING,
            'Latest Version: %s' % message
        ]
    else:
        sb = [
            'Failed to check for updates:',
            message,
            '',
            'Current Version: %s' % VERSION_STRING,
        ]
    print_ln('\n'.join(sb))