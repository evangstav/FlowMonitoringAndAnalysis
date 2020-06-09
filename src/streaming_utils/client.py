# import libraries
from vidgear.gears import NetGear
import cv2

# define netgear client with `receive_mode = True` and default settings
client = NetGear(receive_mode=True, address="10.0.0.1", port=1234)

# infinite loop
while True:
    print("Started Streaming")
    # receive frames from network
    frame = client.recv()

    # check if frame is None
    if frame is None:
        print("No frame")
        # if True break the infinite loop
        break

    # do something with frame here
    print("Receive Frame")
    # Show output window
    # cv2.imshow("Output Frame", frame)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close client
client.close()
