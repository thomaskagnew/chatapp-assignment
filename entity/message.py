# message entity defn

from .entity import Entity

class Message(Entity):
    table_name = "message"
    id: int
    message_type: str
    message: str
    chatroom_id: int
    sender: str

    def __init__(self, id, message_type, message, chatroom_id, sender):
        super().__init__(self.table_name, id=id, message_type=message_type, message=message, chatroom_id=chatroom_id, sender=sender)


    @staticmethod
    def from_json(json):
        return Message(None, json["message_type"], json["message"], json["chatroom_id"], json["sender"])

