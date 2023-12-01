#### SIMPLE CHATAPP
Uses python's websocket library

# accepts
{
    "type": "<message_type>",
    "username": "",
    ... other properties specific to message_type
}

# message_type
1. login
    eg.
    {
        "type": "login",
        "username": "username"
    }
2. createchatroom
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
            "name": "chatroom_name"
        }
3. listchatrooms
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
        }
4. leavechatroom
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
            "chatroom_id": 1
        }
5. enterchatroom
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
            "chatroom_id": 1
        }
6. sendmessage
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
            "chatroom_id": 1
            "message_type": "" -- either text or attachment
            "message": "msg"
        }
7. listmessages
    eg. 
        {
            "type": "createchatroom",
            "username": "usenrame",
            "chatroom_id": 1
        }
