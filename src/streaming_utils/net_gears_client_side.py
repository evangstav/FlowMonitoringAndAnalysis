import numpy as np
import time
from vidgear.gears import NetGear
import cv2
import uuid
from influxdb import InfluxDBClient
from data_rate import DataRate
import argparse


# Instantiate the parser
parser = argparse.ArgumentParser(description="Serve Video to certain IP")
# Optional argument
parser.add_argument(
    "--influxdb_host", type=str, default="localhost",
)
parser.add_argument(
    "--influxdb_port", type=int, default=8086,
)
parser.add_argument(
    "--delay_prob", type=float, default=0.5,
)
# Parse
args = parser.parse_args()

# define netgear client with `receive_mode = True` and default settings
# address should be client side address
# activate Bidirectional mode
options = {"bidirectional_mode": True}  # needed to pass message

client = NetGear(logging=True, protocol="udp", receive_mode=True, **options)
data_rate = DataRate()

# influxdb setup
influxdb_client = InfluxDBClient(host=args.influxdb_host, port=args.influxdb_port)
# Creates the database if it doesnt' exist
influxdb_client.create_database("MainDatabase")
measurement_name = "Cat"
batch_size = 80
influx_data = []
# infinite loop
tic = time.time()
while True:
    n_bytes_1 = data_rate.get_rx_bytes()
    id = str(uuid.uuid4())
    if len(influx_data) > batch_size:
        # print(influx_data)
        influxdb_client.write_points(
            influx_data,
            database="MainDatabase",
            batch_size=batch_size,
            time_precision="u",  # micro secs
            protocol="line",
        )
        influx_data = []
    # add random delay
    if np.random.random() > args.delay_prob:
        random_delay = round(np.random.random() / 10, 2)
        time.sleep(random_delay)
    else:
        random_delay = 0
    # receive frames from network
    data = client.recv()
    if data is None:
        break
    toc = time.time()
    n_bytes_2 = data_rate.get_rx_bytes()

    # Current FPS
    fps = 1 / (toc - tic)
    # Current Data Rate
    rx_rate = round((n_bytes_2 - n_bytes_1) / ((toc - tic) * 1024.0 * 1024.0), 4)

    # reset clock
    tic = toc

    # receive frame and timestamp
    received_timestamp, frame = data
    print(received_timestamp)

    # check if frame is None
    if frame is None:
        # if True break the infinite loop
        break

    # Measured Delay
    delay = (time.time_ns() - received_timestamp) / 1e6  # to milliseconds
    print(f"Delay: {delay} ms")
    # do something with frame here
    # print(int(meta) - int(dt.utcnow().strftime("%s")))

    # store data
    influx_data.append(
        f"{measurement_name},random_delay={random_delay} fps={fps},delay={delay},data_rate={rx_rate}"  # data rate
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
