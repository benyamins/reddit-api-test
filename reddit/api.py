from typing import Dict, Any, Union, List, Tuple
from dataclasses import dataclass
from base64 import b64encode
from datetime import datetime, timedelta
import logging

import requests
from requests.exceptions import HTTPError

from .settings import REDDIT_URL, REDDIT_AUTH_URL, config, SUPPORTED_SECTIONS, LOGGING_LEVEL

# Keep track of
# 'x-ratelimit-remaining' : Number of requests done
# 'x-ratelimit-used'      : Requests left to use
# 'x-ratelimit-reset'     : Number of sec. to en period.


logger: logging.Logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)

logger.setLevel(LOGGING_LEVEL)

@dataclass
class Payload:
    data: Dict[str, str]
    header: Dict[str, str]

@dataclass
class Token:
    """
    Hold the token data, provided by reddit.
    The request returns:
        {'access_token': '469969-75msnOI',
         'token_type': 'bearer',
         'expires_in': 3600,
         'scope': '*'}
    """
    access_token: str
    expires_in: float
    expires_at: datetime = None
    requested_time: datetime = None
    requests_remaining: int = None
    requests_used: int = None
    requests_reset_time: float = None

class TokenLimitError(Exception):
    """ Token expired or can't be used """

class SectionNotSupported(Exception):
    """ The specified secction is not supported. See SUPPORTED_SECTIONS."""

class RedditConnect:
    """
    This class manages the connection & actions.
    """


    def __init__(self) -> None:
        self.username: str = config['auth']['uname']
        self.password: str = config['auth']['password']
        self.client_id: str = config['auth']['client_id']
        self.client_secret: str = config['auth']['secret']
        self.user_agent: str = config['auth']['uagent']
        self.token = self._gen_token()

    def __str__(self) -> str:
        return self.username

    def __repr__(self) -> str:
        output = [
            f'\tUser:{self.username}',
            f'\tReqRemaining:{self.token.requests_remaining}',
            f'\tExpiresAt:{self.token.expires_at}',
            f'\tReqResetTime:{self.token.requests_reset_time}'
        ]
        return '\n'.join(output)

    def _gen_payload(self, token: bool=False) -> Payload:
        basic_auth_encode: str = 'Basic ' + b64encode(
            str.encode(':'.join((self.client_id, self.client_secret)))
        ).decode()

        payload = Payload(
            data={
                'grant_type': 'password',
                'username': self.username,
                'password': self.password,
            },
            header={
                'User-Agent': self.user_agent,
                'Authorization': basic_auth_encode
            }
        )

        if token:
            if self.token.requests_remaining == 0:
                raise TokenLimitError(
                    'No more requests remaining to use for current token'
                    f'Reset time in {self.token.requests_reset_time}'
                )

            if self.token.expires_at < datetime.now():
                self._gen_token(refresh=True)

            payload.header['Authorization'] = f'bearer {self.token.access_token}'

        return payload


    def _gen_token(self, refresh: bool=False) -> Token:

        # Check lifetime of token then return false so query
        # uses existing or refresh it

        payload: Payload = self._gen_payload()

        if refresh:
            payload.data['grant-type'] = 'refresh_token'
            payload.data['refresh-token'] = self.token.access_token

        requested_time = datetime.now()
        response: requests.Response = requests.post(
            f'{REDDIT_URL}/api/v1/access_token',
            data=payload.data,
            headers=payload.header
        ).json()

        return Token(
            access_token=response['access_token'],
            expires_in=response['expires_in'],
            requested_time=requested_time,
            expires_at=requested_time+timedelta(seconds=response['expires_in'])
        )


    def query(self,
            endpoint: str, 
            after: str=None) -> Tuple[List[Dict[str, Any]], str]:
        """
        Parameters
        ----------
            endpoint : one of reddit user section.
                Specified in the SUPPORTED_SECTIONS.
            after : A reddits "Fullname", which is a combination of
                a things type and a unique ID: t3_ + xe32zy.
                This will tell reddit wich listing i want.

        Returns
        -------
            Tuple[ListingData, Fullname]: Fullname can be passed again to this
                function to return the next listing.

        Example
        -------
            >>> connection = RedditConnect()
            >>> connection.query('saved')
            ([{<data>}], 't3_xe32zy')
            >>> connection.query('saved', 't3_xe32zy')
            ([{<data>}], 't3_15bfi0')
        """

        payload: Payload = self._gen_payload(token=True)

        if endpoint not in SUPPORTED_SECTIONS:
            sections = '\n\t' + '\n\t'.join(SUPPORTED_SECTIONS)
            logger.debug("\nThe supported sections are:\n\n"
                    f"{sections}\n")
            raise SectionNotSupported

        params = {'after': after}

        response: requests.Response = requests.get(
            f'{REDDIT_AUTH_URL}/user/{self.username}/{endpoint}',
            headers=payload.header,
            params=params
        )

        response_header: Dict[str, Any] = response.headers

        try:
            self.token.requests_remaining = int(float(response_header['x-ratelimit-remaining']))
            self.token.requests_used = int(float(response_header['x-ratelimit-used']))
            self.token.requests_reset_time = float(response_header['x-ratelimit-reset'])
        except KeyError as err:
            # TODO: logging.info("Fooo", exc_info=True)
            print(err)
            print('\nStatus Code:', response.status_code)
            print('\nHeaders:', response.headers)
            print('\nPayload', payload)
            print('\nParams', params)
        
        response_data: Dict[str, Any] = response.json()

        posts = [post['data'] for post in response_data['data']['children']]

        return posts, response_data['data']['after'], response_data

