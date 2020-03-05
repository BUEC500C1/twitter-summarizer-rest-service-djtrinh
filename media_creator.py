import requests
import subprocess
import datetime
import textwrap
import os
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


class media_creator():

    def __init__(self):
        #Constructor
        pass

    def create_images(self, user_id, user_img_url, tweet, count):
        try:
            txt = tweet.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            try:
                txt = tweet.full_text
            except AttributeError:
                print("Invalid username or tweet grab was corrupted\n")
                return
        background = Image.new('RGBA', (1024, 768), (255, 255, 255, 255))
        font = ImageFont.truetype(r'font/Arial.ttf', 14)
        # fetch user profile pic
        response = requests.get(user_img_url)
        img = Image.open(BytesIO(response.content))
        draw = ImageDraw.Draw(background)
        background.paste(img, (50, 150))
        # Create Twitter tweet text wrapped
        lines = textwrap.wrap(txt, width=120)
        x, y = 50, 225
        for line in lines:
            draw.text(((x), y), line, font=font, fill="black")
            y += 15
        draw.text((120, 170), user_id, font=font, fill="black")
        # Draw final image with tweet and user profile, etc
        self.save_to_file(background, img, user_id, count)

    def fetch_and_save_images(self, tweet, background, y_offset):
        img_list = []
        try:
            if 'media' in tweet.entities:
                for medium in tweet.entities['media']:
                    img_list.append(medium['media_url'])
            if len(img_list) != 0:
                response = requests.get(img_list[0])
                img = Image.open(BytesIO(response.content))
                background.paste(img, (100, y_offset))
        except Exception as e:
            print(e)
        return img_list

    def save_to_file(self, background, img, user_id, count):
        background.save('./processed_imgs/' + str(user_id) + str(count) + '.png')

    def ffmpeg_call(self, username):
        # Cat date with our file name
        today = str(datetime.date.today()).replace('-', '_')
        try:
            subprocess.call(['./ffmpeg/bin/ffmpeg', '-y', '-r', '1/3', '-i', './processed_imgs/'+username+'%d.png',
                           '-pix_fmt', 'yuv420p', '-r', '25', '-loglevel', 'error', '-hide_banner',
                           'twitter_feed_' + username + '_' + today + '.mp4'], stdout=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
            print("Done with " + username + " video! File at "+ os.getcwd() + r'\twitter_feed_' + username + '_' + today + '.mp4')
            print("Twitter id? (x to exit) ", end='')
            today = str(datetime.datetime.now())
            log = open("log_file.txt", 'a')
            log.write(today + ": " + "Finished with video processing of " + username + "\n")
            log.close()
        except Exception as e:
            print("FFMPEG subprcess call had an issue. Most likely had bad tweets from Twitter")
            print(e)
