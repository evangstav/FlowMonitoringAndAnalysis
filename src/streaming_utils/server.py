# import libraries
from vidgear.gears import VideoGear
from vidgear.gears import NetGear

stream = VideoGear(
    source="/home/evangelos/Videos/Cat.mp4").start()  # Open any video stream
server = NetGear(port=1234)  # Define netgear server with diefault settings

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

        # send frame to server
        server.send(frame)

    except KeyboardInterrupt:
        # break the infinite loop
        break

# safely close video stream
stream.stop()
# safely close server
server.close()
