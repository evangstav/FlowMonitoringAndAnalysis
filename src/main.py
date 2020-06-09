import socket

from streaming_utils import camera

virtual_cam = camera.VideoCamera()

frame_1 = virtual_cam.get_frame()
frame_2 = virtual_cam.get_frame()
frame_3 = virtual_cam.get_frame()

msg = virtual_cam.get_frame_bytes()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((socket.gethostname(), 1234))
server.listen(5)

while True:
    clientsocket, address = server.accept()
    print(f"Connection from {address} has been established")
    clientsocket.send(msg)
    clientsocket.close()
