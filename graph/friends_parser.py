import vk_api
from time import sleep
import json

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
for user_id in IDs:
    try:
        friends = vk.friends.get(user_id = user_id)['items']
        for friend in friends:
            if friend not in IDs:
                edges.append([int(user_id), friend])
        sleep(0.35)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'Ошибка с профилем {user_id}: {e}\n')
"""
first_friends = set(edge[1] for edge in edges)

print(len(first_friends))

for user_id in first_friends:
    try:
        second_friends = vk.friends.get(user_id = user_id)['items']
        for friend in second_friends:
            if friend not in first_friends:
                edges.append([int(user_id), friend])
        sleep(0.35)
    except Exception as e:
        with open('logs.txt', 'a') as logs:
            logs.write(f'Ошибка с профилем {user_id}: {e}\n')
"""
data = json.dumps(edges)
print(len(edges))
with open('result.txt', 'w') as file:
    file.write(data)

