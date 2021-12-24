import psycopg2

connection = psycopg2.connect(
    host="172.17.0.2",
    port="5432/tcp",
    database="history_now",
    user="db_user",
    password='testpwd',
)
connection.set_session(autocommit=True)


def is_admin(username: str) -> bool:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                admin
            FROM
                users
            WHERE
                username = '%s'
        """ % username)
        result = cursor.fetchone()
    admin, = result
    return admin

