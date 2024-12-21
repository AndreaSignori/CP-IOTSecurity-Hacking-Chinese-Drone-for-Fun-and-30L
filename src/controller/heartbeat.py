import socket
import time

class Heartbeat:
    def __init__(self, udp_conn: socket.socket, dst_ip: str, dst_port: int, msg: bytes, interval: int) -> None:
        self._socket = udp_conn
        self._dst_ip = dst_ip
        self._dst_port = dst_port
        self._msg = msg
        self._interval = interval

    def send_heartbeat(self) -> None:
        while True:
            print("Sending heartbeat...")
            self._socket.sendto(self._msg, (self._dst_ip, self._dst_port))

            time.sleep(self._interval)