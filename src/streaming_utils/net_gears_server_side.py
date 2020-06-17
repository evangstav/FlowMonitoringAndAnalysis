# import libraries
import time
from vidgear.gears import VideoGear
from vidgear.gears import NetGear
from datetime import datetime as dt
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description="Serve Video to certain IP")
# Optional argument
parser.add_argument(
    "--address", type=str, default="0.0.0.0",
)

# Parse
args = parser.parse_args()

stream = VideoGear(
    resolution=(1920, 1080), source="/home/evangelos/Videos/Cat.mp4",
).start()  # Open any video stream
server = NetGear(
    # address should be client side address
    address=args.address,
    logging=True,
    protocol="udp",
)  # Define netgear server with default settings

# infinite loop until [Ctrl+C] is pressed
while True:
    try:
        frame = stream.read()
        # read frames

        # check if frame is None
        if frame is None:
            # if True break the infinite loop
            break

        # do something with frame here
        timestamp = time.time_ns()
        print(timestamp)

        # send frame to server
        # print(frame)
        server.send(frame, message=timestamp)

    except KeyboardInterrupt:
        # break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
server.close()
