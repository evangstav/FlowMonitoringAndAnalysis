import socket
import cv2
import numpy as np
import matplotlib.pyplot as plt

HOSTNAME = socket.gethostname()
PORT = 5009
HEADER_SIZE = 20

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOSTNAME, PORT))

while True:
    full_msg = ""
    new_message = True
    while True:
        data = s.recv(500000)
        # print(data)
        np_data = np.frombuffer(data, np.uint8)
        frame = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        cv2.imshow("frame", frame)
        cv2.waitKey()

        # if new_message:
        # print(f"new_message length: {msg[:HEADER_SIZE]}")
        # msglen = int(msg[:HEADER_SIZE])
        # new_message = False

        # # print("full message length: ", msg[:HEADER_SIZE])
        # full_msg += msg.decode("utf-8")
        # # print(len(full_msg))

        # if len(full_msg) - HEADER_SIZE == msglen:
        # print("Full message received")
        # # print(full_msg[HEADER_SIZE:])
        # new_message = True
        #     full_msg = ""
