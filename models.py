from clcrypto import hash_password
from connection import connect


class Users:
    def __init__(self, username="", password="", salt=""):
        self._id = -1
        self.username = username
        self.hashed_password = password

    @property
    def id(self):
        return self._id

    @property
    def hashed_password(self):
        return self._hashed_password

    def set_password(self, password):
        self._hashed_password = hash_password(password)

    @hashed_password.setter
    def hashed_password(self, password):
        self.set_password(password)

    def __str__(self):
        return f"Username: {self.username}, Hashed password: {self._hashed_password}"

    def __repr__(self):
        return f"Username: {self.username}, Hashed password: {self._hashed_password}"

    def safe_to_db(self):
        if self._id == -1:
            query = f"INSERT INTO users(username, hashed_password) VALUES ('{self.username}'," \
                    f"'{self._hashed_password}') RETURNING id;"
        else:
            query = f"UPDATE users SET username='{self.username}'," \
                    f"hashed_password='{self._hashed_password}'" \
                    f"WHERE id={self._id};"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        if self._id == -1:
            id_ = cursor.fetchone()[0]
            self._id = id_
        cursor.close()

    @staticmethod
    def load_user_by_id(seek_id):
        query = f"SELECT * FROM users WHERE id={seek_id}"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            loaded_id, seek_username, hashed_password = data
            loaded_user = Users(seek_username)
            loaded_user._id = loaded_id
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_username(seek_username):
        query = f"SELECT * FROM users WHERE username='{seek_username}'"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchone()
        if data:
            loaded_id, seek_username, hashed_password = data
            loaded_user = Users(seek_username)
            loaded_user._id = loaded_id
            loaded_user._hashed_password = hashed_password
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users():
        query = "SELECT * FROM users;"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        if data:
            users = []
            for user in data:
                loaded_id, seek_username, hashed_password = user
                loaded_user = Users(seek_username)
                loaded_user._id = loaded_id
                loaded_user._hashed_password = hashed_password
                users.append(loaded_user)
            return users
        else:
            return None

    def delete(self):
        query = f"DELETE FROM users WHERE id={self._id};"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        self._id = -1
        return True


class Messages:
    def __init__(self, from_id, to_id, text, creation_date=None):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = creation_date

    @property
    def id(self):
        return self._id

    def __str__(self):
        return f"From: {self.from_id}, to: {self.to_id}, message: {self.text}"

    def __repr__(self):
        return f"From: {self.from_id}, to: {self.to_id}, message: {self.text}"

    def safe_to_db(self):
        if self._id == -1:
            query = f"INSERT INTO messages(from_id, to_id, text) VALUES " \
                    f"('{self.from_id}', '{self.to_id}', '{self.text}') RETURNING id;"
        else:
            query = f"UPDATE messages SET from_id='{self.from_id}'," \
                    f"to_id='{self.to_id}', text='{self.text}'" \
                    f"WHERE id={self._id};"
        connection = connect()
        cursor = connection.cursor()
        cursor.execute(query)
        if self._id == -1:
            id_ = cursor.fetchone()[0]
            self._id = id_
        cursor.close()

    @staticmethod
    def load_all_messages(id_=None):
        if id_:
            query = f"SELECT * FROM messages WHERE to_id={id_};"
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(query)
        else:
            query = "SELECT * FROM messages;"
            connection = connect()
            cursor = connection.cursor()
            cursor.execute(query)
            data = cursor.fetchall()
        if data:
            messages = []
            for message in data:
                loaded_id, from_id, to_id, text, creation_date = message
                loaded_message = Messages(from_id, to_id, text)
                loaded_message._id = loaded_id
                loaded_message.creation_date = creation_date
                messages.append(loaded_message)
            return messages
        else:
            return None


if __name__ == '__main__':
    m1 = Messages(5, 8, 'oki doki')
    m1.safe_to_db()
