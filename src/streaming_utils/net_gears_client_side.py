import numpy as np
import time
from vidgear.gears import NetGear
import cv2
import uuid
from influxdb import InfluxDBClient

# define netgear client with `receive_mode = True` and default settings
# address should be client side address

# activate Bidirectional mode
options = {"bidirectional_mode": True}

client = NetGear(logging=True, protocol="udp", receive_mode=True, **options)

# influxdb setup
influxdb_client = InfluxDBClient(host="localhost", port=8086)
influxdb_client.create_database("Test Database")
measurement_name = "Client"
batch_size = 100
influx_data = []
# infinite loop
tic = time.time()
while True:
    id = str(uuid.uuid4())
    print(len(influx_data))
    if len(influx_data) > batch_size:
        influxdb_client.write_points(
            influx_data,
            database="Test Database",
            batch_size=batch_size,
            time_precision="u",  # micro secs
            protocol="line",
        )
        influx_data = []
    # add random delay
    random_delay = time.sleep(np.random.random() / 11)
    # receive frames from network
    data = client.recv()
    if data is None:
        break
    toc = time.time()

    # Current FPS
    fps = 1 / (toc - tic)
    # reset clock
    tic = toc

    # receive frame and timestamp
    received_timestamp, frame = data

    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # Measured Delay
    delay = time.time_ns() - received_timestamp
    # do something with frame here
    # print(int(meta) - int(dt.utcnow().strftime("%s")))

    # store data
    influx_data.append(
        f"{measurement_name},random_delay={random_delay},id={id} fps={fps},delay={delay} {int(time.time()*1000)}"
    )

    # Show output window
    cv2.imshow("Output Frame", frame)
    # print(frame)

    key = cv2.waitKey(1) & 0xFF
    # check for 'q' key-press
    if key == ord("q"):
        # if 'q' key-pressed break out
        break

# close output window
cv2.destroyAllWindows()
# safely close client
client.close()
