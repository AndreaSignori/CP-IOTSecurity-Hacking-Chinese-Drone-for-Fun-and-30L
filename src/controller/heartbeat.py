import socket
import time

class Heartbeat:
    def __init__(self, udp_conn: socket.socket, dst_ip: str, dst_port: int, msg: bytearray, interval: int) -> None:
        """
        :param udp_conn: socket used to connect to the target drone
        :param dst_ip: ip address of the target drone
        :param dst_port: port of the target drone
        :param msg: heartbeat message
        :param interval: interval between heartbeats in second
        """
        self._socket = udp_conn
        self._dst_ip = dst_ip
        self._dst_port = dst_port
        self._msg = msg
        self._interval = interval

    def send_heartbeat(self) -> None:
        """
        Send the heartbeat message every self._interval seconds.
        """

        while True:
            print("Sending heartbeat...")
            self._socket.sendto(self._msg, (self._dst_ip, self._dst_port))

            time.sleep(self._interval)