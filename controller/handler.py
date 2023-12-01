# handle the request and response
import websockets
import json
import asyncio
import logging

from service import chatroom

# connected users
users = {}


async def login(websocket, message):
    # login user
    users[message["username"]] = websocket
    logging.info(f"User {message['username']} logged in")
    await websocket.send(json.dumps({"type": "login", "success": True}))


async def create_chatroom(websocket, message):
    newchatroom = chatroom.create_chatroom(message)
    logging.info(f"Created chatroom {newchatroom.name}")
    await websocket.send(json.dumps({"type": "createchatroom", "success": True}))


async def list_chatrooms(websocket, message):
    chatrooms = chatroom.list_chatrooms()
    await websocket.send(json.dumps({"type": "listchatrooms", "chatrooms": [croom.to_json() for croom in chatrooms]}))


async def leave_chatroom(websocket, message):
    try:
        if message["username"] not in users:
            raise Exception("User not logged in")
        e_chatroom = chatroom.leave_chatroom(message["username"], message["chatroom_id"])
        await websocket.send(json.dumps({"type": "leavechatroom", "chatroom": e_chatroom.to_json()}))
    except Exception as e:
        await websocket.send(json.dumps({"type": "leavechatroom", "success": False, "message": str(e)}))


async def enter_chatroom(websocket, message):
    try:
        if message["username"] not in users:
            raise Exception("User not logged in")
        e_chatroom = chatroom.enter_chatroom(message["username"], message["chatroom_id"])
        await websocket.send(json.dumps({"type": "enterchatroom", "chatroom": e_chatroom.to_json()}))
    except Exception as e:
        await websocket.send(json.dumps({"type": "enterchatroom", "success": False, "message": str(e)}))


async def send_message(websocket, message):
    try:
        if message["username"] not in users:
            raise Exception("User not logged in")
        msg = chatroom.send_message(message)
        await websocket.send(json.dumps({"type": "sendmessage", "message": msg.to_json()}))
    except Exception as e:
        await websocket.send(json.dumps({"type": "sendmessage", "success": False, "message": str(e)}))


async def list_messages(websocket, message):
    try:
        if message["username"] not in users:
            raise Exception("User not logged in")
        messages = chatroom.list_messages(message["chatroom_id"])
        await websocket.send(json.dumps({"type": "listmessages", "messages": [msg.to_json() for msg in messages]}))
    except Exception as e:
        await websocket.send(json.dumps({"type": "listmessages", "success": False, "message": str(e)}))


async def handler(websocket):
    while True:
        try:
            data = await websocket.recv()
            message = json.loads(data)
            if message["type"] == "login":
                await login(websocket, message)
            elif message["type"] == "createchatroom":
                await create_chatroom(websocket, message)
            elif message["type"] == "listchatrooms":
                await list_chatrooms(websocket, message)
            elif message["type"] == "leavechatroom":
                await leave_chatroom(websocket, message)
            elif message["type"] == "enterchatroom":
                await enter_chatroom(websocket, message)
            elif message["type"] == "sendmessage":
                await send_message(websocket, message)
            elif message["type"] == "listmessages":
                await list_messages(websocket, message)
            else:
                raise Exception("Invalid message type")
        except json.decoder.JSONDecodeError as e:
            logging.error("Invalid JSON", e.message)
        except websockets.exceptions.ConnectionClosed:
            logging.info("Connection closed")
        except Exception as e:
            logging.error(e)
            await websocket.send(json.dumps({"type": "error", "message": str(e)}))
