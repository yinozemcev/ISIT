from time import sleep, perf_counter
from requests import get
from pickle import dump
from datetime import datetime

MAX_REQUESTS = 25
V = 5.131
TIMEOUT = 0.33
with open('token.txt') as file:
    ACCESS_TOKEN = file.read().rstrip()

def getRequest(uids: str) -> dict:
    try:
        response = get(f'https://api.vk.com/method/execute.getFriends?&access_token={ACCESS_TOKEN}&uids={uids}&v={V}')
    except Exception as err:
        print(f'Произошла ошибка: {err}')
        return None
    return response.json()

def getFriends(ID_list: list) -> list:
    parts = (','.join(ID_list[i:i+MAX_REQUESTS]) for i in range(0, len(ID_list), MAX_REQUESTS)) if len(ID_list) > MAX_REQUESTS else [','.join(ID_list)]
    result = []
    for part in parts:
        start = perf_counter()
        response = getRequest(part)
        if response:
            result.extend(response['response'])
            elapsed = perf_counter() - start
            sleep(TIMEOUT - elapsed if elapsed < TIMEOUT else 0)
    return result

def process_friends(response: list, edges: dict, all_unique: set) -> list:
    unique = set()
    for i in range(0, len(response), 2):
        edges[response[i]] = set(response[i+1]['items'])
        for elem in response[i+1]['items']:
            unique.add(str(elem))
            all_unique.add(elem)
    return list(unique)

def save(data: dict):
    timestamp = datetime.now().strftime('%d_%m_%Y__%H_%M_%S')
    with open(f'result_{timestamp}.pickle', 'wb') as file:
        dump(data, file)

def main(depth=2):
    with open('IDs.txt') as file:
        unique_friends = file.read().split('\n')

    edges = dict()
    all_unique = set()
    while depth > 0:
        response = getFriends(unique_friends)
        unique_friends = process_friends(response, edges, all_unique)
        depth-=1

    recover_response = getFriends(unique_friends)
    last_unique_friends = set(unique_friends)
    for i in range(0, len(recover_response), 2):
        recovered = set(recover_response[i+1]['items']) & all_unique
        if recovered:
            edges[recover_response[i]] = recovered

    save(edges)
    
if __name__ == '__main__':
    main(1)
