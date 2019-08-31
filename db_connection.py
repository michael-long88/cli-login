import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def drop_table(conn, drop_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param drop_table_sql: a DROP TABLE statement
    """
    try:
        c = conn.cursor()
        c.execute(drop_table_sql)
    except Error as e:
        print(e)


def create_user(conn, user):
    """
        Create a new user into the users table
        :param conn:
        :param user:
        :return: user id
        """
    sql = ''' INSERT INTO users(username,password)
                  VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    return cur.lastrowid


def update_user(conn, user):
    """
        update username, and password of a user
        :param conn:
        :param user:
        :return: user id
        """
    sql = ''' UPDATE users
                  SET username = ? ,
                      password = ?
                  WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()


def get_all_users(conn):
    """
        Query all rows in the users table
        :param conn: the Connection object
        """
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")

    rows = cur.fetchall()

    return rows


def get_user_by_username(conn, username):
    """
        Query users by username
        :param conn: the Connection object
        :param username: username of the user
        """
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))

    rows = cur.fetchall()

    return rows


def delete_user(conn, user_id):
    """
        Delete a user by user id
        :param conn:  Connection to the SQLite database
        :param user_id: id of the user
        """
    sql = 'DELETE FROM users WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (user_id,))
    conn.commit()


def delete_all_users(conn):
    """
    Delete all rows in the users table
    :param conn: Connection to the SQLite database
    :return:
    """
    sql = 'DELETE FROM users'
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()

#
# def main():
#     database = r"C:\Users\N97653\sqlite\db\pythonsqlite.db"
#
#     sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
#                                         id integer PRIMARY KEY,
#                                         username text NOT NULL,
#                                         password text
#                                     ); """
#
#     # create a database connection
#     conn = create_connection(database)
#
#     # create tables
#     if conn is not None:
#         # create users table
#         create_table(conn, sql_create_users_table)
#     else:
#         print("Error! cannot create the database connection.")
#
#
# if __name__ == '__main__':
#     main()
