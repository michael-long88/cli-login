import db_connection
import bcrypt
import yaml


class User:
    def __init__(self, user_id: int, username: str, password: str):
        self._user_id = user_id
        self._username = username
        self._password = password

    @property
    def user_id(self):
        return self._user_id

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, new_username):
        self._username = new_username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, new_password):
        self._password = new_password


class Login:
    def __init__(self):
        with open('db.yaml', 'r') as db_config:
            self.db_config = yaml.safe_load(db_config)
        self.database_path = self.db_config['DEV_PATH']
        self.user = None
        self.logged_in = False
        self.create_user_table()

    def create_user_table(self):
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                                id integer PRIMARY KEY,
                                                username text NOT NULL,
                                                password text
                                            ); """

        with db_connection.create_connection(self.database_path) as conn:
            if conn is not None:
                db_connection.create_table(conn, sql_create_users_table)
            else:
                print("Error! Cannot create the database connection.")

    def login(self):
        for i in range(3):
            print(f"Attempt {i + 1} / 3")
            username = input("Username: ")
            password = input("Password: ")
            if self.login_user(username, password):
                break
        else:
            print("Too many attempts.")

    def login_user(self, username: str, password: str, database: str = None) -> bool:
        if database is None:
            database = self.database_path
        with db_connection.create_connection(database) as conn:
            user_rows = db_connection.get_user_by_username(conn, username)
            user_id, user_username, user_password = user_rows[0]
            if user_rows and bcrypt.checkpw(password.encode('utf8'), user_password):
                self.user = User(user_id, user_username, user_password)
                self.logged_in = True
                print("Successful login")
                return True
        return False

    def logout(self):
        self.user = None
        self.logged_in = False

    def update_password(self):
        if self.is_logged_in():
            old_password = input("Enter old password: ")
            new_password = input("Enter new password: ")
            confirm_new_password = input("Confirm new password: ")
            if self.is_password_valid(old_password, new_password, confirm_new_password):
                self.update_user_password(new_password)
            elif not self.is_matching_password(new_password, confirm_new_password):
                print("Passwords didn't match. Try again.")
                self.update_password()

    def is_logged_in(self) -> bool:
        return self.logged_in

    def is_password_valid(self, old_password: str, new_password: str, confirmed_password: str) -> bool:
        if self.is_matching_password(new_password, confirmed_password) and bcrypt.checkpw(old_password.encode('utf8'),
                                                                                          self.user.password):
            return True
        return False

    def is_matching_password(self, password: str, confirmed_password: str) -> bool:
        if password == confirmed_password:
            return True
        else:
            return False

    def update_user_password(self, new_password: str, database: str = None):
        if database is None:
            database = self.database_path
        new_hashed_password = bcrypt.hashpw(new_password.encode('utf8'), bcrypt.gensalt())
        with db_connection.create_connection(database) as conn:
            db_connection.update_user(conn, (self.user.username, new_hashed_password, self.user.user_id))
        self.user.password = new_hashed_password

        print("Password updated.")

    def register(self):
        username, password = self.create_credentials()
        hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        self.create_new_user((username, hashed_password))

    def create_credentials(self, username: str = "") -> tuple:
        if username == "":
            username = input(f"Username: ")
        else:
            print(f"Username: {username}")
        password = input("Password: ")
        confirm_password = input("Confirm password: ")
        if password != confirm_password:
            print("The passwords don't match. Please try again.")
            self.create_credentials(username)
        elif self.user_exists(username):
            print("That username already exist")
            choice = input("[T]ry again or [L]ogin?").upper()
            if choice == "T":
                self.create_credentials()
            else:
                self.login()
        return username, password

    def user_exists(self, username: str, database: str = None) -> bool:
        if database is None:
            database = self.database_path
        with db_connection.create_connection(database) as conn:
            user_rows = db_connection.get_user_by_username(conn, username)
            if len(user_rows) == 0:
                return False
            else:
                return True

    def create_new_user(self, credentials: tuple, database: str = None):
        if database is None:
            database = self.database_path
        with db_connection.create_connection(database) as conn:
            user_id = db_connection.create_user(conn, credentials)
        self.user = User(user_id, credentials[0], credentials[1])
        self.logged_in = True
        print(f"User {self.user.user_id} with username {self.user.username} has been created and logged in.")

    def deactivate_account(self, database: str = None):
        if database is None:
            database = self.database_path
        user_id = self.user.user_id
        with db_connection.create_connection(database) as conn:
            db_connection.delete_user(conn, user_id)
        self.user = None
        self.logged_in = False
