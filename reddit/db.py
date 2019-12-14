from .settings import DATABASE, MODULE_PATH, SUPPORTED_SECTIONS
from pathlib import PosixPath
from typing import List, Any, Tuple, Union
from .utils import Colors

import sqlite3 as sql
import sys
import logging

logger: logging.Logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler()

logger.addHandler(stream_handler)

logger.setLevel(logging.DEBUG)

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
        ('NumComments', 'INTEGER')
    ]

    def __init__(self,
                table_name: str=None, 
                db_name: PosixPath=DATABASE) -> None:
        self.db_name = db_name
        self.table_name = table_name if table_name is not None else self._last_used()
        self._check_db()


    def _get_db(self) -> sql.Connection:
        """ self.db_name
        """
        db: sql.Connection = sql.connect(self.db_name)
        return db


    def _init_db(self) -> None:

        logger.debug(f'Initializing DB: {self.db_name}')
        logger.debug('Creating LastUsed & ExistingTables')

        db: sql.Connection = self._get_db()
        db.execute('CREATE TABLE LastUsed (Id INTEGER PRIMARY KEY, TableName TEXT)')
        db.execute('CREATE TABLE ExistingTables (Id INTEGER PRIMARY KEY, TableName TEXT)')
        db.commit()
        db.close()


    def _insert_or_update(self, query: str, args: List[Any]=[]) -> None:
        # See this needs another abstraction on top
        # in case the insert query preparation is done on
        # this class or the api
        # TODO: maybe this isn't a private class.

        logger.debug(f'{Colors.WARNING}_insert_or_update:'
                f' ===== \n  {query} \n===== \n{Colors.ENDC}')

        with self._get_db() as db:
            db.execute(query, args)
        db.close()


    def select_db(self) -> str:
        # TODO: there seems to be a problem. How do i abstract the selection.

        logger.debug(f'{Colors.WARNING}select_db: self.table_name{Colors.ENDC}')

        db: sql.Connection = self._get_db()
        result: sql.Cursor = db.execute("SELECT * FROM LastUsed")
        if not result.fetchall():
            _insert_or_update(
                "INSERT INTO LastUsed (TableName) VALUES (?)", [self.table_name]
            )
        else:
            _insert_or_update("UPDATE LastUsed SET TableName = ?", [self.table_name])


    def query(self, query: str, args: List[Any]=[]) -> List[Any]:
        db: sql.Connection = self._get_db()
        cursor: sql.Cursor = db.cursor()
        result: List[Any] = cursor.execute(query, args).fetchall()
        db.close()

        return result

    def _insert_section(self, args: List[Any]) -> None:
        """
            Insert to a secction table
            pass only the arguments to the insert operation
        """

        columns = ','.join(column[0] for column in DBConnection.column_names)

        query = f"""
        INSERT INTO {self.table_name} ({columns})
        VALUES
            ({','.join('?' for _ in range(len(DBConnection.column_names)))})
        """

        self._insert_or_update(query, args)
    

    def _create_table(self) -> None:

        columns = ','.join(
            f'{column[0]} {column[1]}' for column in DBConnection.column_names
        )

        logger.debug(f'Creating Table with column: {columns}')

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
        with self._get_db() as db:
            db.execute(create_query)
            self._insert_or_update(inser_query, [self.table_name])
        db.close()


    def _check_db(self) -> None:
        """ 
        Check if self.db_name && self.table exists.
        else create them
        """

        logger.debug(f"\n{Colors.WARNING}Checking DB{Colors.ENDC}\n")

        if self.table_name not in SUPPORTED_SECTIONS:
            raise SelectedTableError('Section Not Supported, Check Settings')

        elif not self.db_name.exists():
            print(f'Creating DB & Table {self.db_name.name}')
            self._init_db()
            self._create_table()
            return None

        elif self.db_name.exists():
            db: sql.Connection = self._get_db()
            result: sql.Cursor = db.execute(
                "SELECT * FROM sqlite_master WHERE name = ?", [self.table_name]
            )

            if not result.fetchall():
                print(f'Creating table {self.db_name.name}')
                self._create_table()

            db.close()


    def _last_used(self) -> str:
        try:
            last_used: List[Tuple[str]] = self.query('SELECT TableName FROM LastUsed') 
        except sql.OperationalError as err:
            raise SelectedTableError("The DB hasnt been initialize")
        if not last_used:
            raise SelectedTableError('No last used table and no table_name was provided')
        else:
            last_used: str = last_used[0][0]

        return last_used


if __name__ == '__main__':
    # TODO: THIS SHOULD BE ON TEST!!
    # foo = DBConnection('saved')
    foo = DBConnection('saved')
    args = ['https://how.com', 'SomeTitle', '/r/golang', 'https://foo', 42132.32, 120, 'Author',
            107, 2]
    foo._insert_section(args)
    res: List[Any] = foo.query('SELECT * FROM saved')


