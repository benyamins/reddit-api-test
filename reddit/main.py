from typing import List, Dict, Any
import logging

from .api import RedditConnect, Content
from .db import DBConnection
from .settings import LOGGING_LEVEL

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

logger: logging.Logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)

logger.setLevel(LOGGING_LEVEL)


def get_content():

    section = "saved"

    reddit = RedditConnect()

    db_con = DBConnection("saved")

    print("queryng")
    content: Content = reddit.query(section)

    saved = []

    while content.after:

        for data in content.data:
            links = [
                data["url"],
                data["title"],
                data["subreddit"],
                data["permalink"],
                data["created_utc"],
                data["score"],
                data["author"],
                data["gilded"],
                data["num_comments"],
                data["name"],
            ]
            saved.append(links)

        logger.debug(
            f"len : {len(content.data)}-listing : {content.after}"
            f"-response : {content.response}"
            f"-requests_remaining : {reddit.token.requests_remaining}"
            f"-len_saved : {len(saved)}"
        )

        content: Content = reddit.query(section, content.after)

    logger.debug(
        f"len : {len(content.data)}-listing : {content.after}"
        f"-response : {content.response}"
        f"-requests_remaining : {reddit.token.requests_remaining}"
        f"-len_saved : {len(saved)}"
    )

    db_con.insert_section(saved, many=True)
