#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
import uuid
from websockets.asyncio.client import connect
import os

async def hello(random):
    async with connect("ws://localhost:8765") as websocket:
        await websocket.send(f"Hello world! {random}")
        message = await websocket.recv()
        print(message)


#get list of gpx files in diectory
#ask user whichone to choose
#"downlaod" and extract actual points (send 1 point per second - not the best but ok)

def get_gpx_file():
    os.chdir("gpx_files")
    all_files = os.listdir()
    gpx_files = [f for f in all_files if f.endswith('.gpx')]
    print("Available GPX files:")
    #print(gpx_files)    
    for i, file in enumerate(gpx_files):
        print(f"{i + 1}: {file}")
    choice = int(input("Enter the number of the GPX file you want to choose(num/\"RND\"): "))
    #check if value is RND
    if choice == "RND":
        import random
        choice = random.randint(0, len(gpx_files) - 1)
    else:
        choice -= 1  # Adjust for zero-based index
    
    selected_file = gpx_files[choice]
    print("*" * 20)
    print(f"You selected: {selected_file}")

if __name__ == "__main__":
    # random = uuid.uuid4()

    # while True:
    #     asyncio.run(hello(random))

    get_gpx_file()