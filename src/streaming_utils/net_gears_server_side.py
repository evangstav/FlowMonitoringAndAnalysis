# import libraries
import time
from vidgear.gears import VideoGear, CamGear
from vidgear.gears import NetGear
from datetime import datetime as dt
import argparse
import cv2

# Instantiate the parser
parser = argparse.ArgumentParser(description="Serve Video to certain IP")
# Optional argument
parser.add_argument(
    "--address", type=str, default="0.0.0.0",
)
# Parse
args = parser.parse_args()
source = "udpsrc port=5000 ! application/x-rtp,media=video,encoding-name=JPEG! rtpjpegdepay ! jpegdec ! videoconvert !video/x-raw, format=BGR !appsink"
# source = "rtsp://192.168.20.7:5000/"
stream = CamGear(
    source=source, backend="1800", logging=True
).start()  # Open any video stream
server = NetGear(
    # address should be client side address
    address=args.address,
    logging=True,
    protocol="tcp",
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
