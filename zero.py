import time

import zmq

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5000")

print("Client started")
i = 0
while True:
    socket.send_string(f"Current iteration is: {i}")
    msg = socket.recv_string()
    print("Received message %s" % msg)
    time.sleep(1)
    i += 1
