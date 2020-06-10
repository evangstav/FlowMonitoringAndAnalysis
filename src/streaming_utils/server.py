import socket
from camera import VideoCamera

HEADER_SIZE = 100
PORT = 5009

# Create socket and listen on port 5005
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("", PORT))
server_socket.listen(5)

v_cam = VideoCamera()

while True:
    client_socket, address = server_socket.accept()
    print(f"Connection from {address} established.")
    msg = v_cam.get_frame_bytes()
    # header = f"{len(msg):<{HEADER_SIZE}}"  #:< is left alignement
    # msg = "".join([header, str(msg)])
    client_socket.sendall(msg)
    client_socket.close()
