import numpy as np
import time
from vidgear.gears import NetGear
import cv2

FPS_list = []

# define netgear client with `receive_mode = True` and default settings
# address should be client side address

# activate Bidirectional mode
options = {"bidirectional_mode": True}

client = NetGear(logging=True, protocol="udp", receive_mode=True, **options)

# infinite loop
tic = time.time()
while True:
    # receive frames from network
    data = client.recv()
    if data is None:
        break
    toc = time.time()
    print(toc - tic)
    print("FPS: ", 1 / (toc - tic))
    FPS_list.append(1 / (toc - tic))
    tic = toc
    meta, frame = data
    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # do something with frame here
    # print(int(meta) - int(dt.utcnow().strftime("%s")))

    # Show output window
    cv2.imshow("Output Frame", frame)
    # print(frame)
    print(meta)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close client
client.close()
print("Average FPS: ", np.mean(FPS_list))
print("Max FPS: ", np.max(FPS_list))
print("Min FPS: ", np.min(FPS_list))
