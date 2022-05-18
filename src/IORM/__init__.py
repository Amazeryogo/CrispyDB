import sqlite3


class IORM:
    def __init__(self, db):
        self.db = db
        self.conn = sqlite3.connect(self.db)
        self.cursor = self.conn.cursor()

    def create_table(self, table, schema):
        """
        Create a table in the database
        """
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} ({})".format(table, schema)
        )
        self.conn.commit()

    def drop_table(self, table):
        """
        Drop a table in the database
        """
        self.cursor.execute("DROP TABLE IF EXISTS {}".format(table))
        self.conn.commit()

    def insert(self, table, data):
        """
        Insert data into a table
        """
        keys = ', '.join(data.keys())
        values = ', '.join(['?'] * len(data))
        sql_query = 'INSERT INTO {} ({}) VALUES ({})'.format(table, keys, values)
        self.cursor.execute(sql_query, tuple(data.values()))
        self.conn.commit()

    def fetch(self, table, columns='*', where=None):
        """
        Fetch data from a table
        """
        if where:
            sql_query = "SELECT {} FROM {} WHERE {}".format(columns, table, where)
        else:
            sql_query = "SELECT {} FROM {}".format(columns, table)
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def update(self, table, data, where):
        """
        Update data in a table
        """
        update = ', '.join(['{} = ?'.format(k) for k in data])
        sql_query = 'UPDATE {} SET {} WHERE {}'.format(table, update, where)
        self.cursor.execute(sql_query, tuple(data.values()))
        self.conn.commit()

    def delete(self, table, where):
        """

        :param table:
        :param where:
        :return:
        """
        sql_query = 'DELETE FROM {} WHERE {}'.format(table, where)
        self.cursor.execute(sql_query)
        self.conn.commit()
