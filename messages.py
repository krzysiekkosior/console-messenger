import argparse
from clcrypto import check_password
from models import Users, Messages

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--password', help='password')
parser.add_argument('-t', '--to', help='to (username)')
parser.add_argument('-s', '--send', help='text of message')
parser.add_argument('-l', '--list', help='list all messages sent to you', action='store_true')
args = parser.parse_args()


def list_messages(username, password):
    user = Users.load_user_by_username(username)
    if user:
        if check_password(password, user.hashed_password):
            messages = Messages.load_all_messages(user._id)
            count = 1
            for message in messages:
                from_user = Users.load_user_by_id(message.from_id)
                print(f"{count}. {from_user.username}: {message.text}")
                count += 1
        else:
            print("Incorrect password.")
    else:
        print("User does not exist.")


def send_message(username, password, to_username, text):
    user = Users.load_user_by_username(username)
    if user:
        if check_password(password, user.hashed_password):
            to_user = Users.load_user_by_username(to_username)
            if to_user:
                message = Messages(user.id, to_user.id, text)
                message.safe_to_db()
                print("Message sent.")
            else:
                print("User you are trying to send message to does not exist.")
        else:
            print("Incorrect password.")
    else:
        print("User does not exist.")


if args.username and args.password and args.list:
    list_messages(args.username, args.password)
elif args.username and args.password and args.to and args.send:
    send_message(args.username, args.password, args.to, args.send)
else:
    parser.print_help()
