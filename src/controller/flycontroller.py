import socket
import time
import threading

from src.controller.heartbeat import Heartbeat


class FlyController:
    def __init__(self, dst_ip: str, dst_port: int, heartbeat_interval: int, heartbeat_msg: bytes, buffer_size: int):
        self._dst_ip: str = dst_ip
        self._dst_port: int = dst_port
        self._buffer_size: int = buffer_size
        self._heartbeat: Heartbeat|None = None
        self._heartbeat_interval: int = heartbeat_interval
        self._heartbeat_msg: bytes = heartbeat_msg
        self._udp_socket: socket.socket|None = None

    def start(self) -> bool:
        if self._udp_socket is None:
            self._udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # heartbeat mechanism implementation
            self._heartbeat = Heartbeat(self._udp_socket, self._dst_ip, self._dst_port, self._heartbeat_msg, self._heartbeat_interval)

            beating =  threading.Thread(target=self._heartbeat.send_heartbeat)
            beating.start()

            return True
        return False
    def stop(self) -> None:
        self._udp_socket.close()
        self._udp_socket = None

    def send(self, data: bytes) -> int:
        if not self._udp_socket is None:
            return self._udp_socket.sendto(data, (self._dst_ip, self._dst_port))
        else:
            return -1

    def receive(self) -> bytes:
        # TODO: valutare meccanismo di timeout
        data, _ = self._udp_socket.recvfrom(self._buffer_size)

        #TODO: analisi dati ricevuti
        #print(data)
        return data

if __name__ == '__main__':
    controller = FlyController(dst_ip='127.0.0.1', dst_port=20001, heartbeat_interval=1, heartbeat_msg=bytearray([1, 1]),buffer_size=1024)
    
    if controller.start():
        print('Sending greetings message')
        controller.send(b'hello')
        time.sleep(30)
        controller.stop()
