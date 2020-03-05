import threading
import time
import queue
import twitter_api as twit
import glob
import os
import os.path
import media_creator
import datetime
import sys


# Thread that processes create image requests. 4 of these are run
def processor(q, mc):
    while (True):
        item = q.get()
        # Do not create image item grabbed is blank
        if item is not None:
            mc.create_images(item[0], item[1], item[2], item[3])
            today = str(datetime.datetime.now())
            log = open("log_file.txt", 'a')
            log.write(today + ": " + str(item[0]) + " image processing in progress...\n")
            log.close()
        q.task_done()
        time.sleep(.001)


# ffmpeg subprocess thread function that calls ffmpeg when files are ready
def ffpmeg_processor(q2, mc):
    while (True):
        username = q2.get()
        # Do not check for images if username is blank
        if username is not None:
            png_count = len(glob.glob1(r"processed_imgs/", username + r"*.png"))
            today = str(datetime.datetime.now())

            if png_count < 20:
                q2.put(username)
            else:
                log = open("log_file.txt", 'a')
                log.write(today + ": " + username + " video processing in progress...\n")
                log.close()
                mc.ffmpeg_call(username)
        q2.task_done()
        time.sleep(.001)


# thread function that puts creation of image task to the queue
def producer(q, q_item):
    # the main thread will put new items to the queue
    for count, tweet in enumerate(q_item[2]):
        q.put([q_item[0], q_item[1], tweet, count])
    q.join()


# Command line interface
def cli(q1, q2):
    while(True):
        id = input("Twitter id? (x to exit) ")
        if id.lower() == 'x':
            sys.exit();
        elif id != '':
            # Remove old pictures with matching Twitter ID
            filelist = glob.glob(os.path.join(r'processed_imgs/', id + "*.png"))
            if len(filelist) > 0:
                for f in filelist:
                    os.remove(f)
            # Create processes to start generating pictures
            q_item = [id, twit.get_user_pic(id), twit.get_users_tweets(id)]
            t = threading.Thread(name="ProducerThread", target=producer, args=(q1, q_item))
            q2.put(id)
            t.start()
        else:
            print("Please enter a valid ID\n")


if __name__ == '__main__':
    # create queue
    q1 = queue.Queue(maxsize=4)
    q2 = queue.Queue()

    # create media class which has functions that create images and videos
    mc = media_creator.media_creator()

    # grab keys
    twit = twit.twitter_scrapper("keys")

    # 4 threads to do processes running at .001 seconds . This will create the images
    threads_num = 4
    for i in range(threads_num):
        t = threading.Thread(name="Thread Processor-" + str(i), target=processor, args=(q1, mc,))
        t.start()

    # FFMPEG thread
    # Checks if images are there and creates the mp4 file if the criteria is met
    t = threading.Thread(name="FFMPEG Processor", target=ffpmeg_processor, args=(q2, mc,))
    t.start()

    # CLI thread
    t = threading.Thread(name="CLI", target=cli, args=(q1, q2,))
    t.start()
