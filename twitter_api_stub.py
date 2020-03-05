import json
import sys


class twitter_api_stub():


    def __init__(self):
        self.j = json.load(open("google.json"))

    def get_user_pic(self, username):
        if username == "Google":
            return self.j['user']['profile_image_url_https']
        else:
            print("400", file=sys.stderr)
            return ""

    def get_users_tweets(self, username):
        if username == "Google":
            return self.j["full_text"]
        else:
            print("400", file=sys.stderr)
            return ''

    def grab_pictures(self, username):
        if username == "Google":
            return self.j['media']
        else:
            print("400", file=sys.stderr)
            return []