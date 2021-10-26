import json
import requests

class Vksearch:

    def check_account(self, user_id):
        with open('vktoken.txt') as file:
            vktoken = file.read().strip()
        url = "https://api.vk.com/method/users.get"
        params = {
            "user_ids": {user_id},
            "fields": "bdate, sex, city, relation",
            "access_token": vktoken,
            "v": "5.131",
        }

        response = requests.get(url=url, params=params)
        main_keys = dict()

        # if 'response' in response.json():
        if 'error' not in response.json():
            for info in response.json()['response']:
                keys = {'bdate', 'sex', 'city', 'relation'} & info.keys()
                for key in keys:
                    main_keys[key] = info[key]

            if 'bdate' in main_keys:
                if len(main_keys['bdate']) > 5:
                    main_keys['bdate'] = main_keys['bdate'][-4:]
                else:
                    del main_keys['bdate']

            return main_keys
        else:
            return 0


    def find_users(self, user_id):
        info_user = self.check_account(user_id)
        if info_user == 0:
            return 0
        else:
            pair_users = []
            with open('vktoken.txt') as file:
                vktoken = file.read().strip()
            url = "https://api.vk.com/method/users.search"
            params = {
                "fields": "bdate, sex, city, relation",
                "count": '1000',
                "access_token": vktoken,
                "v": "5.131"
            }
            response = requests.get(url=url, params=params)
            users = response.json()['response']['items']

            with open('users.json', 'w', encoding='utf-8') as file:
                json.dump(users, file, ensure_ascii=False)

            for user in users:
                if user['sex'] != info_user['sex']:
                    if 'relation' in user and user['relation'] != 3 and user['relation'] != 4:
                        if 'city' in user and 'city' in info_user and 'bdate' in user and 'bdate' in info_user:
                            if user['city'] == info_user['city']:
                                if info_user['bdate'] == user['bdate'][-4:]:
                                    pair_users.append(user)
                        elif 'city' in user and 'city' in info_user:
                            if 'bdate' not in info_user:
                                if user['city'] == info_user['city']:
                                    pair_users.append(user)
                        elif 'bdate' in user and 'bdate' in info_user:
                            if info_user['bdate'] == user['bdate'][-4:]:
                                pair_users.append(user)
            return pair_users


    def find_top_photo(self, user_id):
        users = self.find_users(user_id)
        if users == 0:
            return 0
        elif len(users) == 0:
            return 1
        elif len(users) >= 1:
            photo_href = dict()
            main_dict = dict()
            for user in users:
                currend_id_user = user['id']
                with open("vktok.txt") as file:
                    vktoken = file.read().strip()
                url = "https://api.vk.com/method/photos.get"
                params = {
                    "user_id": currend_id_user,
                    "access_token": vktoken,
                    "v": "5.131",
                    "album_id": "profile",
                    "extended": "1"
                }
                response = requests.get(url=url, params=params)
                photograph = response.json()["response"]["items"]
                for photo in photograph:
                    user_href = f"https://vk.com/id{photo['owner_id']}"
                    photo_href[photo["sizes"][-3]["url"]] = photo["likes"]["count"]
                top_photo = sorted(photo_href.items(), key=lambda x: x[1], reverse=True)
                main_dict[user_href] = top_photo[:3]
                photo_href.clear()
            return main_dict


# if __name__ == '__main__':
#     vkinder = Vksearch()
#     vkinder.find_top_photo('liza_nikolaevna_0327')
