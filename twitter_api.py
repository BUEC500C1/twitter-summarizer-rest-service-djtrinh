import tweepy
import configparser


class twitter_scrapper():

    def __init__(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        auth = tweepy.OAuthHandler(config.get('auth', 'consumer_key').strip(),
                                   config.get('auth', 'consumer_secret').strip())
        auth.set_access_token(config.get('auth', 'access_token').strip(),
                              config.get('auth', 'access_secret').strip())
        self.api = tweepy.API(auth)

    def get_user_pic(self, username):
        try:
            u = self.api.get_user(username)
            return u.profile_image_url_https
        except tweepy.error.TweepError as e:
            print(e)
            return ""

    def get_users_tweets(self, username):
        try:
            tweets = self.api.user_timeline(screen_name=username, count=20, include_rts=True, result_type="recent",
                                    include_entities=True,
                                    tweet_mode='extended',
                                    lang="en")
            return tweets
        except tweepy.error.TweepError as e:
            print(e)
            return ""

    def grab_pictures(self, username):
        img_list = []
        try:
            for tweet in tweepy.Cursor(self.api.search,
                                       q=username,
                                       count=100,
                                       result_type="recent",
                                       include_entities=True,
                                       tweet_mode='extended',
                                       lang="en").items():
                if 'media' in tweet.entities:
                    for medium in tweet.entities['media']:
                        if medium['type'] == 'photo':
                            img_list.append(medium['media_url'])
            return img_list
        except tweepy.error.TweepError as e:
            print(e)
            return img_list
