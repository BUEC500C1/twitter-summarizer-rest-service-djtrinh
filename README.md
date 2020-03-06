# Twitter to Video

### Introduction
In this project, we will be creating a multi-threaded application that picks the top 20 tweets from a Twitter handle and makes a 60 sec video out of it.
Every 3 seconds, the top tweet will be shown along with their profile picture and username. Currently, the application is a single
process running with 4 threads. The output format is a 1024x768 resolution mp4 file running at 25 frames per second. Each of the 4
threads is responsible for image processing, specifically creating the backgroud, drawing the username, user picture and writing the
tweet for all twenty images.

### Computer Evaluation

In my current computer configuration, I have a 6-core processor with 12 threads and a maximum clock rate of 4.1 Ghz. As a result of this, I am really unable to see any bottlenecks when running code conversion tests which were the following:

```python
ffmpeg.exe -i test.mp4 -c:a copy -c:v copy -r 30 -s hd720 -b:v 2M output.mp4
```

```python
ffmpeg.exe -i test.mp4 -c:a copy -c:v copy -r 30 -s hd480 -b:v 1M output.mp4
```

Each of the commands on a 3 minute test video finished in < 1 seconds. Because of this, we will be running the program with 4 threads which is overkill.

### How to Run?
EC2 Server: ec2-18-189-26-79.us-east-2.compute.amazonaws.com/

This application requires primarily Tweepy, Python 3, and other packages specified in the requirements.txt file.

Please make sure all APIs have been installed before running the program. To run the program, run sudo python3 flaskapp.py. 
Twitter keys must be in the root program directory named keys. The following is the format needed.

```python
[auth]
consumer_key = ****
consumer_secret = ****
access_token = ****
access_secret = ****
```

Originally, this project was a CLI interface. The project has been changed to become restful. To run it we can do the following commands:

```python

curl http://ec2-18-189-26-79.us-east-2.compute.amazonaws.com/user/Google

```

The user can specify which user they want to create a video of. When the server receives this command,
20 requests are queued for the 4 threads to start creating images all running asychronously.
The FFMPEG thread creates the final video when all images are completed.

To view the final video, one would follow the link given by the previous command.

In this case, it is the following:

```python

curl ec2-18-189-26-79.us-east-2.compute.amazonaws.com/video/twitter_feed_Google_2020_03_06.mp4

```

If a video is not ready yet, a statement saying so will be printed instead. Otherwise, the video player is shown.
The user can also save the video if they so desire.

The following screenshots is the restful server in action and working:

<img src="https://github.com/BUEC500C1/twitter-summarizer-rest-service-djtrinh/blob/master/restful_picture.PNG?raw=true">

-------------------------------------------------------------------------------------------------------------------------

<img src="https://github.com/BUEC500C1/twitter-summarizer-rest-service-djtrinh/blob/master/Example2.PNG?raw=true">

### Conclusion
There are more additions that can be done with with the server. Currently, it is run on an Amazon EC2 Ubuntu server. However, what we can
do is actually implement a more user friendly interface. As a result, the user does not have to manually enter the commands. On the flip side, having the user be able to manually makes calls allows others to easily utilize the functionality for their application.
