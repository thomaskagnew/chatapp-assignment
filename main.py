import asyncio
import websockets
import os 
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from controller import handler
from repository import db

# setup logging
logging.basicConfig(level=logging.INFO)


async def main():
    async with websockets.serve(handler.handler, "", 8001):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    db.connect()
    db.init_db()
    asyncio.run(main())
