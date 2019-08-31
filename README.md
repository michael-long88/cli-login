# cli-login

CLI login system that can:
- register new users with a username and password
- login existing users
- allow a user to logout
- allow a user to change their password if they're logged in
- allow a user to deactivate their account (removing it from the database)

Passwords are salted and hashed using `bcrypt` before being stored in a SQLite database.

## Getting Started
Necessary libraries are in `requirements.txt`, which can be install with the command `pip install -r requirements.txt`. The location of the SQLite database will be stored in `db.yaml`. Create the `db.yaml` file with the following line, replacing the text with the desired location of the SQLite database: `C:\Users\%username%\sqlite\db\cli-login.db`

This will only create the SQLite file, not any parent directories (like `\sqlite\db`) which will need to be created manually.
