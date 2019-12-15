from typing import List, Dict, Any

from .api import RedditConnect
from .db import DBConnection

"""
            UploadedUrl TEXT,   --url
            Title TEXT,         --title
            Subreddit TEXT,     --subreddit
            RedditLink TEXT,    --permalink
            CreateDate REAL, --created_utc
            Upvoted INTEGER     --score
            Author TEXT, --author
            Gilded INTEGER --gilded
            NumComments INTEGER --num_comments
            FullName --name

"""


def foo():

    section = 'comments'

    reddit = RedditConnect()

    saved_data: List[Dict[str, Any]]
    next_listing: str 

    print('queryng')
    saved_data, next_listing, res = reddit.query(section)
    print(res)

    from pprint import pprint
    print(len(saved_data))
    pprint(saved_data[0])

    while next_listing:

        saved = []

        for data in saved_data:
            links = [
                data['url'],
                data['title'],
                data['subreddit'],
                data['permalink'],
                data['created_utc'],
                data['score'],
                data['author'],
                data['gilded'],
                data['num_comments'],
                data['name']
            ]
            saved.append(links)

        # for i, e in enumerate(saved):
            # print(i, e[2], e[9])

        saved_data, next_listing, res = reddit.query(section, next_listing)



def data_base():


    con = DBConnection()

    res = con.query('select * from saved')

    for e in res: print(e)


if __name__ == '__main__':
    foo()
