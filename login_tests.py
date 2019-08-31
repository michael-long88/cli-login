import unittest
import db_connection
import bcrypt
import login
import yaml


class TestLogin(unittest.TestCase):
    def setUp(self):
        with open('db.yaml', 'r') as db_config:
            self.db_config = yaml.safe_load(db_config)
        self.database_path = self.db_config['TEST_PATH']
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                                id integer PRIMARY KEY,
                                                username text NOT NULL,
                                                password text
                                            ); """
        # create a database connection
        self.conn = db_connection.create_connection(self.database_path)
        if self.conn is not None:
            # create users table
            db_connection.create_table(self.conn, sql_create_users_table)
        else:
            print("Error! cannot create the database connection.")

        self.login_session = login.Login()

    def tearDown(self):
        sql_drop_users_table = "DROP TABLE IF EXISTS users;"

        # create a database connection
        self.conn = db_connection.create_connection(self.database_path)
        if self.conn is not None:
            # drop users table
            db_connection.drop_table(self.conn, sql_drop_users_table)
        else:
            print("Error! cannot create the database connection.")

    def test_login(self):
        username = "testUser"
        password = "password"
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        with db_connection.create_connection(self.database_path) as conn:
            db_connection.create_user(conn, (username, hashed_password))

        self.login_session.login_user(username, password, self.database_path)

        self.assertTrue(self.login_session.logged_in, 'Not logged in')

    def test_matching_passwords(self):
        password = "password"
        confirm_new_password = "password"

        is_matching = self.login_session.is_matching_password(password, confirm_new_password)

        self.assertTrue(is_matching, "Passwords do not match")

    def test_valid_passwords(self):
        self.create_test_user()

        old_password = "password"
        new_password = "new_password"
        confirm_new_password = "new_password"

        is_valid = self.login_session.is_password_valid(old_password, new_password, confirm_new_password)

        self.assertTrue(is_valid, "Password is not valid")

    def test_logout(self):
        self.create_test_user()

        self.assertTrue(self.login_session.is_logged_in(), "User is not logged in")
        self.assertIsInstance(self.login_session.user, login.User, "No user")

        self.login_session.logout()

        self.assertFalse(self.login_session.is_logged_in(), "User is still logged in")

    def test_password_update(self):
        self.create_test_user()
        old_hashed_password = self.login_session.user.password
        new_password = "new_password"

        self.login_session.update_user_password(new_password)

        self.assertNotEqual(old_hashed_password, self.login_session.user.password, "Password was not updated")

    def test_register_new_user(self):
        username = "newTestUser"
        password = "password"

        self.login_session.create_new_user((username, password), self.database_path)

        self.assertTrue(self.login_session.logged_in, "User was not logged in")
        self.assertIsInstance(self.login_session.user, login.User, "User was not instantiated")
        with db_connection.create_connection(self.database_path) as conn:
            self.assertEqual(1, len(db_connection.get_user_by_username(conn, username)), "User was not created in DB")

    def test_user_exists(self):
        self.create_test_user()
        with db_connection.create_connection(self.database_path) as conn:
            self.assertTrue(self.login_session.user_exists(self.login_session.user.username, self.database_path),
                            "User does not exist")

    def create_test_user(self):
        username = "testUser"
        password = "password"
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        with db_connection.create_connection(self.database_path) as conn:
            user_id = db_connection.create_user(conn, (username, hashed_password))
            self.login_session.user = login.User(user_id, username, hashed_password)
            self.login_session.logged_in = True
