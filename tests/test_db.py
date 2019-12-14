from reddit import DBConnection


def test_db():
    con = DBConnection('saved')

    assert con.db_name == 'saved'
