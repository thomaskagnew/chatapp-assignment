# chatroom entity

from .entity import Entity
from .message import Message
from repository import db


max_users: int = 10


class Chatroom(Entity):
    table_name = "chatroom"
    id: int
    name: str

    def __init__(self, id, name):
        super().__init__(self.table_name, id=id, name=name)

    @staticmethod
    def from_json(json):
        return Chatroom(None, json["name"])

    def save(self):
        if self.is_name_unique():
            super().save()
        else:
            raise Exception("Chatroom name already exists")

    def add_user(self, username):
        if username in self.get_users():
            raise Exception("User already in chatroom")

        if len(self.get_users()) >= max_users:
            raise Exception("Chatroom is full")
        
        cursor = db.get_cursor()
        cursor.execute(f"INSERT INTO chatroom_users (chatroom_id, username) VALUES (%s, %s)", (self.id, username))
        db.commit()

    def get_users(self):
        cursor = db.get_cursor()
        cursor.execute(f"SELECT username FROM chatroom_users WHERE chatroom_id = %s", (self.id,))
        data = cursor.fetchall()
        return [row[0] for row in data]

    def get_messages(self):
        cursor = db.get_cursor()
        cursor.execute(f"SELECT * FROM messages WHERE chatroom_id = %s", (self.id,))
        data = cursor.fetchall()
        return [Message(**dict(zip([column.name for column in cursor.description], row))) for row in data]

    def send_message(self, message):
        message.chatroom_id = self.id
        message.save()

    def remove_user(self, username):
        cursor = db.get_cursor()
        cursor.execute(f"DELETE FROM chatroom_users WHERE chatroom_id = %s AND username = %s", (self.id, username))
        db.commit()

    def is_name_unique(self):
        cursor = db.get_cursor()
        cursor.execute(f"SELECT * FROM {self.table_name}s WHERE name = %s", (self.name,))
        return cursor.fetchone() is None
