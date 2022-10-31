import psycopg2
from crawler import Crawler

host = "heffalump.db.elephantsql.com"
user = 'sdjminza'
password = 'epNcEMj5bgVjhU8RNiVlWngeWDi6SwMR'
database = 'sdjminza'

def db_init():
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database=database
    )
    # print(type(connection))
    if isinstance(connection,psycopg2.extensions.connection):
        print("db connected")
        cursor = connection.cursor()
    if isinstance(cursor,psycopg2.extensions.cursor):
        print("db initiation")

    return connection, cursor

def db_close(connection):
    connection.close()

def update(connection, cursor, data):
    TABLE_WEBTOON = "webtoon"
    TABLE_GENRE = "genre"
    TABLE_ARTIST = "artist"

    query_table_webtoon = f"TRUNCATE TABLE IF EXISTS {TABLE_WEBTOON}"
    # query_table_genre = f"TRUNCATE TABLE IF EXISTS {TABLE_GENRE}"
    # query_table_ARTIST = f"TRUNCATE TABLE IF EXISTS {TABLE_ARTIST}"

    cursor.execute(query_table_webtoon)

    query_create_table = f"""
        CREATE TABLE {TABLE_WEBTOON} (
            id          INTEGER SERIAL PRIMARY KEY,
            title       VARCHAR(128),
            platform    VARCHAR(64),
            link        VARCHAR(128),
            rate        FLOAT,
            for_adult   BOOLEAN,
            views_rank  INTEGER         
        )
    """

def db_update():
    connection, cusor = db_init()
    crawler = Crawler()
    webtoons = crawler.collect_naver_data()



    db_close(connection)





