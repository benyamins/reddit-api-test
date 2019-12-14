from typing import List, Dict, Any

from .api import RedditConnect
from .db import DBConnection

"""
            UploadedUrl TEXT,   --url
            Title TEXT,         --title
            Subreddit TEXT,     --subreddit
            RedditLink TEXT,    --permalink
            CreateDate REAL, --
            Upvoted INTEGER     --ups

            Author TEXT, --author
            Gilded INTEGER --gilded
            NumComments INTEGER --num_comments
"""


def foo():
    reddit = RedditConnect()

    saved_data: List[Dict[str, Any]]
    next_listing: str 

    saved_data, next_listing = reddit.query('saved')

    for post in saved_data:
        post['title']


def data_base():


    con = DBConnection()

    res = con.query('select * from saved')

    for e in res: print(e)


if __name__ == '__main__':
    data_base()
