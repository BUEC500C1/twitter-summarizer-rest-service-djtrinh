import twitter_api as twit
import twitter_api_stub as twit2
import os


def test_valid_userpic(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_user_pic("Google").find("https") == 0


def test_invalid_userpic1(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_user_pic("alksdhfaksdlfj") == ""


def test_invalid_userpic2(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_user_pic("") == ""


def test_invalid_userpic3(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_user_pic(5) == ""


def test_invalid_tweet1(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    captured = capsys.readouterr()
    assert t.get_users_tweets("alksdhfaksdlfj") == ""


def test_invalid_tweet2(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_users_tweets(23) == ""


def test_valid_tweet():
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.get_users_tweets("Google") != ""


def test_grab_pictures1(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.grab_pictures("alksdhfaksdlfj") == []


def test_grab_pictures2(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.grab_pictures("") == []


def test_grab_pictures3(capsys):
    if os.stat("keys").st_size == 0:
        t = twit2.twitter_api_stub()
    else:
        t = twit.twitter_scrapper("keys")
    assert t.grab_pictures(" ") == []