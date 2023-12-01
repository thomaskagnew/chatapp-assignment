# chatroom service
import secrets

from entity import chatroom
from entity import message

def create_chatroom(chatroomdict):
    newchatroom = chatroom.Chatroom.from_json(chatroomdict)
    newchatroom.save()
    return newchatroom

def list_chatrooms():
    return chatroom.Chatroom(0,"").getall()

def enter_chatroom(username, chatroom_id):
    e_chatroom = chatroom.Chatroom(0,"")
    e_chatroom = e_chatroom.get(chatroom_id)

    if e_chatroom is None:
        raise Exception("Chatroom does not exist")
    e_chatroom.add_user(username)
    return e_chatroom

def leave_chatroom(username, chatroom_id):
    e_chatroom = chatroom.Chatroom(0,"")
    e_chatroom = e_chatroom.get(chatroom_id)

    if e_chatroom is None:
        raise Exception("Chatroom does not exist")
    e_chatroom.remove_user(username)
    return e_chatroom


def handle_attachment(attachment):
    # read attachment and save to file
    file_name = secrets.token_hex(8)
    file_extension = None
    file_path = "root/"

    # open file in write binary mode
    with open(file_path, "wb") as f:
        # initialize magic library
        magic = magic.Magic(mime=True)
        # get file extension
        file_extension = magic.from_buffer(attachment.read(1024))
        # reset file pointer to beginning of file
        attachment.seek(0)
        # write to file
        f.write(attachment)

    # rename file with extension
    os.rename(file_path, file_path + "." + file_extension)

    return "file_path"

def send_message(i_message):
    if i_message["message_type"] == "attachment":
        file_path = handle_attachment(i_message["message"])
        i_message["message"] = file_path

    msg = message.Message.from_json(i_message)
    msg.save()
    return msg

def list_messages(chatroom_id):
    e_chatroom = chatroom.Chatroom(0,"")
    e_chatroom = e_chatroom.get(chatroom_id)

    if e_chatroom is None:
        raise Exception("Chatroom does not exist")
    return e_chatroom.get_messages()
