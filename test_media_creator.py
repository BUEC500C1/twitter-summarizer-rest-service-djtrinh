import media_creator as mc
from PIL import Image


def test_create(capsys):
    m = mc.media_creator()
    m.create_images("aslfdad", "asldkfdf", "asdfasdf", 5)
    captured = capsys.readouterr()
    assert captured.err.find("Invalid username or tweet grab was corrupted")


def test_create2(capsys):
    m = mc.media_creator()
    m.create_images("", "", "", 0)
    captured = capsys.readouterr()
    assert captured.err.find("Invalid username or tweet grab was corrupted")


def test_fetch():
    m = mc.media_creator()
    background = Image.new('RGBA', (1024, 768), (255, 255, 255, 255))
    assert m.fetch_and_save_images("tweet", background, 15) == []


def test_ffmpeg_call(capsys):
    m = mc.media_creator()
    m.ffmpeg_call("test")
    captured = capsys.readouterr()
    assert captured.err.find("no file")


def test_save(capsys):
    m = mc.media_creator()
    background = Image.new('RGBA', (1024, 768), (255, 255, 255, 255))
    m.save_to_file(background, "", "", 0)
    captured = capsys.readouterr()
    assert captured.err == ''
