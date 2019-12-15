from reddit.api import RedditConnect

def test_instance():
    con = RedditConnect()
    assert isinstance(con, RedditConnect) == True
