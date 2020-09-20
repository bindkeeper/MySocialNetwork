#!/usr/bin/env python
import argparse
import os
import random
import requests

NUMBER_OF_USERS = "number_of_users"
MAX_POSTS_PER_USER = "max_posts_per_user"
MAX_LIKES_PER_USER = "max_likes_per_user"

USER_NAME = "username"
EMAIL = "email"
PASSWORD = "password"
POSTS_LEFT = "posts_left"
LIKES_LEFT = "likes_left"

USER_NAME_PREFIX = "user_"

PROTOCOL = "http://"
HOST = "127.0.0.1:8000"
JWT_ENDPOINT = PROTOCOL + HOST + "/api/token/"
POSTS_ENDPOINT = PROTOCOL + HOST + "/posts/"
REGISTER_ENDPOINT = PROTOCOL + HOST + "/users/register"
USERS_ENDPOINT = PROTOCOL + HOST + "/users/"
LIKES_ENDPOINT = PROTOCOL + HOST + "/likes/"


def file_path(path):
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError(path)


def parse_args():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--path', type=file_path, required=True)

    args = parser.parse_args()
    print(args.path)
    return args


def register_user(user):
    payload = {
        USER_NAME: user[USER_NAME],
        EMAIL: user[EMAIL],
        "password": PASSWORD,
        "password_confirm": PASSWORD
    }
    r = requests.post(REGISTER_ENDPOINT, json=payload)
    print("user :" +user[USER_NAME] + " registered")


def login_user(user):
    payload =  {
            EMAIL: user[EMAIL],
            "password": PASSWORD
        }

    r = requests.post(JWT_ENDPOINT, json=payload)
    print(r.json())
    return r.json()["access"]


def create_posts(user, jwt):
    while user[POSTS_LEFT] > 0:
        left = user[POSTS_LEFT]
        user[POSTS_LEFT] = left - 1
        payload = {
            "title": "hello world from " + str(user[USER_NAME]),
            "text": "I have " + str(user[POSTS_LEFT]) + " left",
        }
        headers = {'Authorization': 'Bearer ' + jwt}
        r = requests.post(POSTS_ENDPOINT, headers= headers, json=payload)
        if r.status_code==201:
            print(r.json())


def has_post_with_zero_likes():
    r = requests.get(POSTS_ENDPOINT)
    posts = r.json()
    for post in posts:
        if len(post["likes"]) == 0:
            return True
    return False


def next_user_to_like(users):
    r = requests.get(USERS_ENDPOINT)
    server_users = r.json()
    next_user = None
    for user in server_users:
        user_name = user[USER_NAME]
        if user_name in users and users[user[USER_NAME]][LIKES_LEFT] > 0:
            if not next_user:
                next_user = user
            elif len(next_user["posts"]) < len(user["posts"]):
                next_user = user
    if next_user:
        return users[next_user[USER_NAME]]
    else:
        None


def already_liked_it(user, post_id):
    r = requests.get(POSTS_ENDPOINT  + str(post_id) + "/")
    likes = r.json()['likes']
    for like in likes:
        likes_respons = requests.get(LIKES_ENDPOINT + str(like) + "/")
        likes_owner_response = requests.get(USERS_ENDPOINT + str(likes_respons.json()['owner']) + "/")
        if user[USER_NAME] == likes_owner_response.json()[USER_NAME]:
            return True
    return False


def create_likes(next_user):
    jwt = login_user(next_user)
    headers = {'Authorization': 'Bearer ' + jwt}

    r = requests.get(POSTS_ENDPOINT)
    posts = r.json()
    for post in posts:
        if post["owner"] != next_user[USER_NAME]:
            if not already_liked_it(next_user, post['id']):
                r = requests.post(LIKES_ENDPOINT, headers=headers, json={"post_id": post['id']})
                print("user " + next_user[USER_NAME] + " likes " + str(post['id']))
                next_user[LIKES_LEFT] = next_user[LIKES_LEFT] - 1
                if next_user[LIKES_LEFT] == 0:
                    return


if __name__ == "__main__":
    args = parse_args()

    number_of_users = 0
    max_posts_per_user = 0
    max_likes_per_user = 0

    with open(args.path, "r") as f:
        for line in f:
            if line.startswith(NUMBER_OF_USERS):
                number_of_users = int(line.split("=", 2)[1].strip())
            if line.startswith(MAX_POSTS_PER_USER):
                max_posts_per_user = int(line.split("=", 2)[1].strip())
            if line.startswith(MAX_LIKES_PER_USER):
                max_likes_per_user = int(line.split("=", 2)[1].strip())

    print("number_of_users %d" % number_of_users)
    print("max_posts_per_user %d" % max_posts_per_user)
    print("max_likes_per_user %d" % max_likes_per_user)

    users = {}
    for x in range(0, number_of_users):
        username = USER_NAME_PREFIX+str(x)
        amount_of_posts = random.randint(1, max_posts_per_user)
        users[username] = {
                            USER_NAME: username,
                            EMAIL: username+"@test.com",
                            POSTS_LEFT: amount_of_posts,
                            LIKES_LEFT: max_likes_per_user
                        }

    print(str(users))

    for user in users:
        register_user(users[user])
        jwt = login_user(users[user])
        create_posts(users[user], jwt)
        
    for x in range(0, len(users)):
        next_user = next_user_to_like(users)
        if next_user:
            create_likes(next_user)
        else:
            exit(0)



