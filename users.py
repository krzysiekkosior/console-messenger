import argparse
from psycopg2.errors import UniqueViolation
from clcrypto import check_password, hash_password
from models import Users

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username", help="username")
parser.add_argument("-p", "--password", help="password (min 8 characters)")
parser.add_argument("-n", "--new_pass", help="new password (min 8 characters)")
parser.add_argument("-l", "--list", help="list all users", action="store_true")
parser.add_argument("-d", "--delete", help="delete user", action="store_true")
parser.add_argument("-e", "--edit", help="edit user", action="store_true")
args = parser.parse_args()


def new_user(username, password):
    if len(password) < 8:
        print("Password is too short - must contain min 8 characters.")
    else:
        try:
            new_user = Users(username, password)
            new_user.safe_to_db()
            print("New user added.")
        except UniqueViolation as error:
            print(error)


def new_password(username, password, new_password):
    user = Users.load_user_by_username(username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user._hashed_password):
        if len(new_password) < 8:
            print("New password is too short - must contain min 8 characters.")
        else:
            user._hashed_password = hash_password(new_password)
            user.safe_to_db()
            print("Password changed.")
    else:
        print("Incorrect password.")


def delete_user(username, password):
    user = Users.load_user_by_username(username)
    if not user:
        print("User does not exist.")
    elif check_password(password, user._hashed_password):
        user.delete()
        print("User deleted.")
    else:
        print("Incorrect password.")


def list_of_usernames():
    loaded_users = Users.load_all_users()
    counter = 1
    for user in loaded_users:
        print(f"{counter}. {user.username}")
        counter += 1


if args.username and args.password and args.edit and args.new_pass:
    new_password(args.username, args.password, args.new_pass)
elif args.username and args.password and args.delete:
    delete_user(args.username, args.password)
elif args.username and args.password:
    new_user(args.username, args.password)
elif args.list:
    list_of_usernames()
else:
    parser.print_help()
