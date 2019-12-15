from reddit.db import DBConnection


def test_db():

    con = DBConnection('saved')

    assert con.table_name == 'saved'
