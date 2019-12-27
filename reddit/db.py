from .settings import DATABASE, MODULE_PATH, SUPPORTED_SECTIONS, LOGGING_LEVEL
from pathlib import PosixPath
from typing import List, Any, Tuple, Union
from .utils import clrs

import sqlite3 as sql
import sys
import logging

logger: logging.Logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)

logger.setLevel(LOGGING_LEVEL)

class SelectedTableError(Exception):
    """ Error related to created tables in sqlite3 """

class DBConnection:
    """
    Tables Created:
        LastUsed:        [TableName]
        ExistingTables:  [TableName]
        self.table_name: [UploadedUrl, Title, Subreddit, 
                          Upvoted, CreateDate, RedditLink]
    """

    column_names = [
        ('UploadedUrl', 'TEXT'),
        ('Title', 'TEXT'),
        ('Subreddit', 'TEXT'),
        ('RedditLink', 'TEXT'),
        ('CreateDate', 'REAL'),
        ('Upvoted', 'INTEGER'),
        ('Author', 'TEXT'),
        ('Gilded', 'INTEGER'),
        ('NumComments', 'INTEGER'),
        ('FullName', 'TEXT')
    ]

    def __init__(self,
                table_name: str=None, 
                db_name: PosixPath=DATABASE) -> None:
        self.db_name = db_name
        self.table_name = table_name.lower() if table_name is not None else self._last_used()
        self._check_db()


    def _get_db(self) -> sql.Connection:
        """ self.db_name
        """
        db: sql.Connection = sql.connect(self.db_name)
        return db


    def _init_db(self) -> None:

        logger.debug(f'Initializing DB: {self.db_name}')
        logger.debug('Creating LastUsed & ExistingTables')

        with self._get_db() as db:
            db.execute('CREATE TABLE LastUsed (Id INTEGER PRIMARY KEY, TableName TEXT)')
            db.execute('CREATE TABLE ExistingTables (Id INTEGER PRIMARY KEY, TableName TEXT)')
            db.execute('CREATE TABLE LastListing (Id INTEGER PRIMARY KEY, Listing TEXT)')
        db.close()


    def _insert_or_update(self, query: str, args: List[Any]=[], many=False) -> None:

        logger.debug(f'{clrs.WARNING}_insert_or_update:'
                f' ===== \n  {query} \n===== \n{clrs.ENDC}')

        with self._get_db() as db:
            if many:
                db.executemany(query, args)
            else:
                db.execute(query, args)
        db.close()


    def select_db(self) -> str:
        # TODO: there seems to be a problem. How do i abstract the selection.

        logger.debug(f'{clrs.WARNING}select_db:======\n\n\t{self.table_name}{clrs.ENDC}'
                '\n======')

        db: sql.Connection = self._get_db()
        result: sql.Cursor = db.execute("SELECT * FROM LastUsed")
        if not result.fetchall():
            self._insert_or_update(
                "INSERT INTO LastUsed (TableName) VALUES (?)", [self.table_name]
            )
        else:
            self._insert_or_update("UPDATE LastUsed SET TableName = ?", [self.table_name])


    def query(self, query: str, args: List[Any]=[]) -> List[Any]:
        """
            Parameters
            ----------
                query: String containing a valid sql query.
                args : arguments to pass to the '?' for templating.

            Returns
            -------
                List[PostData[int, float, str]]: A row corresponding to a post.

            Example
            -------
                >>> con = DBConnection()
                >>> con.query('select * from saved where author = ?', ['madeto_be'])
                [('foo', 'bar', '..'), ('baz', 'spam')]
        """
        db: sql.Connection = self._get_db()
        cursor: sql.Cursor = db.cursor()
        result: List[Any] = cursor.execute(query, args).fetchall()
        db.close()

        return result

    def insert_section(self, args: Union[List[Any], List[List[Any]]], many=False) -> None:
        """
            Insert to a secction table
            pass only the arguments to the insert operation

            Parameters
            ----------
                args : Arguments to be passed for insert or bulk insert.
                    If List[List] then many=True must be passed. TODO: Code should know
                    what to use.
                many : Defult uses execute, True uses executemany.

            Returns
            -------
                None

            Example
            -------
                >>> con = DBConnection('saved')  # LastUsed in case of None
                >>> args1 = ['foo', 'bar', '..']
                >>> con.insert_section(args1)
                >>> args2 = [['foo', 'bar', '..'], ['foo2', 'bar2', '..2']]
                >>> con.insert_section(args2, many=True)
        """

        columns = ','.join(column[0] for column in DBConnection.column_names)

        query = f"""
        INSERT INTO {self.table_name} ({columns})
        VALUES
            ({','.join('?' for _ in range(len(DBConnection.column_names)))})
        """

        self.select_db()
        self._insert_or_update(query, args, many)
    

    def _create_table(self) -> None:

        columns = ','.join(
            f'\n\t{column[0]} {column[1]}' for column in DBConnection.column_names
        )

        logger.debug(f'Creating {self.table_name} Table with column: {columns}')

        create_query = f"""
        CREATE TABLE {self.table_name} (
            Id INTEGER PRIMARY KEY,
            {columns}
        )
        """
        inser_query = """
        INSERT INTO ExistingTables (TableName)
        VALUES (?)
        """

        self._insert_or_update(create_query)

        if self.table_name in SUPPORTED_SECTIONS:
            self._insert_or_update(inser_query, [self.table_name])
            self.select_db()


    def _check_db(self) -> None:
        """ 
        Check if self.db_name && self.table exists.
        else create them
        """

        logger.debug(f"\n{clrs.WARNING}Checking DB{clrs.ENDC}\n")

        if self.table_name not in SUPPORTED_SECTIONS:
            raise SelectedTableError('Section Not Supported, Check Settings')

        elif not self.db_name.exists():
            print(f'Creating DB & Table {self.db_name.name}')
            self._init_db()
            self._create_table()
            return None

        elif self.db_name.exists():
            result: List[Any] = self.query(
                "SELECT * FROM sqlite_master WHERE name = ?", [self.table_name]
            )

            if not result:
                print(f'Creating table {self.table_name}')
                self._create_table()



    def _last_used(self) -> str:
        try:
            last_used: List[Tuple[str]] = self.query('SELECT TableName FROM LastUsed') 
        except sql.OperationalError as err:
            raise SelectedTableError("The DB hasnt been initialize")
        if not last_used: # Will never reach this section
            raise SelectedTableError('No last used table and no table_name was provided')
        else:
            last_used: str = last_used[0][0]

        return last_used


class RedditDB(DBConnection):
    pass


if __name__ == '__main__':
    # TODO: THIS SHOULD BE ON TEST!!
    foo = DBConnection('gilded')
    args = ['https://how.com', 'SomeTitle', '/r/golang', 'https://foo', 42132.32, 120, 'Author',
            1, 2, 't3_15bfi0']
    args2 = [
        ['https://how.com', 'SomeTitle', '/r/golang', 'https://foo', 42132.32, 120, 'Author',
            2, 2, 't3_15bfi0'],
        ['https://how.com', 'SomeTitle', '/r/golang', 'https://foo', 42132.32, 120, 'Author',
            3, 2, 't3_15bfi0'],
    ]
    foo.insert_section(args)
    foo.insert_section(args2, many=True)
    res: List[Any] = foo.query('SELECT * FROM gilded')


