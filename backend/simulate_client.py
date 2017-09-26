import requests

#r = requests.post(url='http://127.0.0.1:8000/present_create/', json=present_data)

# create a new user
# new_user_data = {'username': 'Elodie', 'password': 'PASSWORD', 'email': 'WESH@wanadoo.fr'}
# r = requests.post('http://127.0.0.1:8000/user_create/', json=new_user_data)

# # first login
# login_data = {'username': 'Marcel', 'password': 'PASSWORD', 'email': 'bidule4@test.com'}
# r = requests.post('http://192.168.0.12:8000/user_create/', json=login_data)
# print(r.status_code)
# print(r.content)


new_game_data = {'users': [
        {
            "id": 1,
            "score": 35,
        },
        {
            "id": 2,
            "score": 50,
        },
        {
            "id": 3,
            "score": 35,
        }
]
}

r = requests.post('http://192.168.0.12:8000/games/', json=new_game_data)
print(r.status_code)
print(r.content)


# get token
# token = r.json()['token']
# print(token)
#
# # try to delete a present
# headers = {'Authorization': 'Token %s' % str(token)}
# r = requests.put('http://127.0.0.1:8000/present_create/', headers=headers, json=present_pk)
# print(r.status_code)
# print(r.content)



