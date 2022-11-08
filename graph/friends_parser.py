from time import sleep
from requests import get
from json import loads
from pickle import dump
from datetime import datetime

with open('token.txt') as file:
    access_token = file.read().rstrip()

with open('IDs.txt') as file:
    IDs = file.read().split('\n')

def getFriends(IDs):    
    if len(IDs) <= 25:
        uids = ','.join(IDs)
        response = get(f'https://api.vk.com/method/execute.getFriends?&access_token={access_token}&uids={uids}&v=5.131').text
        return loads(response)['response']
    else:
        parts = (','.join(IDs[i:i+25]) for i in range(0, len(IDs), 25))
        result = []
        for part in parts:
            response = get(f'https://api.vk.com/method/execute.getFriends?&access_token={access_token}&uids={part}&v=5.131').text
            result.extend(loads(response)['response'])
            sleep(0.1)
        return result

def process_friends(response, edges, all_unique):
    unique = set()
    for i in range(0, len(response), 2):
        edges[response[i]] = set(response[i+1]['items'])
        for elem in response[i+1]['items']:
            unique.add(str(elem))
            all_unique.add(elem)
    return list(unique)

def save(friends):
    timestamp = datetime.now().strftime('%d_%m_%Y__%H_%M_%S')
    with open(f'result_{timestamp}.pickle', 'wb') as file:
        dump(friends, file)

def main(depth=2):
    edges = {}
    all_unique_friends = set()
    unique_friends = IDs
    while depth > 0:
        response = getFriends(unique_friends)
        unique_friends = process_friends(response, edges, all_unique_friends)
        depth-=1
    recover_response = getFriends(unique_friends)
    for i in range(0, len(recover_response), 2):
        recovered = set(recover_response[i+1]['items']) & all_unique_friends
        if recovered:
            edges[recover_response[i]] = recovered
    save(edges)
    
if __name__ == '__main__':
    main(2)
