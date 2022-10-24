import vk_api
from time import sleep
import pickle
from datetime import datetime

"""
Файл private.txt должен иметь следующее содержание:
Логин (или телефон)
Пароль
ID приложения (app_id)
Ключ доступа (access_token)
"""
with open('private.txt') as file:
    login, password, app_id, access_token = file.read().split('\n')

with open('IDs.txt') as file:
    IDs = file.read().split('\n')

vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()

edges = []
first_friends = []
for user_id in IDs:
    try:
        friends = vk.friends.get(user_id = user_id)['items']
        for friend in friends:
            first_friends.append(friend)
            edges.append((int(user_id), friend))
        sleep(0.35)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'[{datetime.now()}] Ошибка с профилем {user_id}: {e}\n')
"""
first_friends = set(first_friends)
print(len(first_friends))

for user_id in first_friends:
    try:
        second_friends = vk.friends.get(user_id = user_id)['items']
        for friend in second_friends:
            edges.append((int(user_id), friend))
        sleep(0.35)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'[{datetime.now()}] Ошибка с профилем {user_id}: {e}\n')
"""
total_edges = set(tuple(sorted(edge)) for edge in edges)
print(len(total_edges))
timestamp = datetime.now().strftime('%d_%m_%Y__%H_%M_%S')
with open(f'result_{timestamp}.pickle', 'wb') as file:
    pickle.dump(total_edges, file)

