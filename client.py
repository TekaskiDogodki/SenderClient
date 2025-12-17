#!/usr/bin/env python

"""Client using the asyncio API."""

import asyncio
import uuid
from websockets.asyncio.client import connect
import os
import gpxpy
import time
import random

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
    choice = input("Enter the number of the GPX file you want to choose(num/\"RND\"): ")
    #check if value is RND
    if choice == "RND":
        import random
        choice = random.randint(0, len(gpx_files) - 1)
    else:
        choice = int(choice)-1  # Adjust for zero-based index
    
    selected_file = gpx_files[choice]
    print("*" * 20)
    print(f"You selected: {selected_file}")
    return selected_file


async def gpx_points_sender(file_path):
    #get file
    gpx_file = open(file_path, 'r')

    gpx = gpxpy.parse(gpx_file)

    lat_long = []
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                lat_long.append((point.latitude,point.longitude))
    
    print(lat_long[20:30])

    #send lat_long tuple every second
    
    random_id = random.randint(0,1000)

    async with connect("ws://localhost:8765") as websocket:
        
        #wait 1 second
        for point in lat_long:
            await websocket.send(f"{random_id},{point[0]},{point[1]},{time.time()}")
            message = await websocket.recv()
            print(f"Sent point: {point}, Received echo: {message}")
            await asyncio.sleep(1)



if __name__ == "__main__":
    # random = uuid.uuid4()

    # while True:
    #     asyncio.run(hello(random))

    asyncio.run(gpx_points_sender(get_gpx_file()))