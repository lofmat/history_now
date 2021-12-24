import logging
import psycopg2
from psycopg2 import sql

logging.basicConfig(level=logging.NOTSET)


class DBConnector:
    def __init__(self, password, user, db, host, port):
        self.pwd = password
        self.user = user
        self.db = db
        self.host = host
        self.port = port

    # # TODO check connection status https://kb.objectrocket.com/postgresql/get-the-status-of-a-transaction-with-the-psycopg2-python-adapter-for-postgresql-745
    # @contextlib.contextmanager
    def connect(self):
        # Connect to an existing database
        connection = psycopg2.connect(database=self.db,
                                      user=self.user,
                                      password=self.pwd,
                                      host=self.host,
                                      port=self.port)
                                # host="172.17.0.2",
                                # port="5432/tcp")
        return connection

    def insert(self, table: str, columns: list, values: list):
        """
        :param table:
        :param columns: date, tag, news_text
        :param values: list of tuples
        :return:
        """

        connection = self.connect()
        cursor = connection.cursor()
        columns_names = sql.SQL(', ').join(sql.Identifier(n) for n in columns)
        placeholders = sql.SQL(', ').join(sql.Placeholder() * len(columns))

        q = sql.SQL("insert into {table_name} ({col_names}) values ({val})").format(
            table_name=sql.Identifier(table),
            col_names=columns_names,
            val=placeholders
        )
        try:
            logging.info(f"Current query -> {q.as_string(connection)}")
            cursor.execute(q, values)
            connection.commit()
            logging.info(f"Commit for insert: {q.as_string(connection)}")
        except Exception as e:
            logging.exception(f'Exception -> {e}. Query -> {q.as_string(connection)}')
            connection.rollback()
            logging.exception(f'Rollback for insert: {q.as_string(connection)}')
        cursor.close()
        connection.close()

    def _exec_query(self, query):
        logging.info(f'Executing -> {query}')
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        res = ''
        try:
            res = cursor.fetchall()
        except psycopg2.ProgrammingError:
            logging.warning('Nothing to fetchone')
        cursor.close()
        connection.close()
        return res
