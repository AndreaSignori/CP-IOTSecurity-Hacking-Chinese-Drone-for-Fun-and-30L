import socket
import threading

from src.controller.heartbeat import Heartbeat


class FlyController:
    def __init__(self, dst_ip: str, dst_port: int, heartbeat_interval: int, heartbeat_msg: bytearray, buffer_size: int):
        """
        :param dst_ip: ip address of the target drone
        :param dst_port: port of the target drone
        :param heartbeat_interval: time interval between heartbeats in second
        :param heartbeat_msg: message to send to the target drone as heartbeat
        :param buffer_size: buffer size for receiving response from the drone
        """
        self._dst_ip: str = dst_ip
        self._dst_port: int = dst_port
        self._buffer_size: int = buffer_size
        self._heartbeat: Heartbeat|None = None
        self._heartbeat_interval: int = heartbeat_interval
        self._heartbeat_msg: bytearray = heartbeat_msg
        self._udp_socket: socket.socket|None = None

    def start(self) -> bool:
        """
        Start the controller in order to be capable to send and receive messages  and the heartbeat mechanism

        :return: If the controller was started successfully or not
        """
        if self._udp_socket is None:
            self._udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

            # heartbeat mechanism implementation
            self._heartbeat = Heartbeat(self._udp_socket, self._dst_ip, self._dst_port, self._heartbeat_msg, self._heartbeat_interval)

            beating =  threading.Thread(target=self._heartbeat.send_heartbeat)
            beating.start()

            return True
        return False

    def stop(self) -> None:
        """
        Stop the controller closing the socket
        """

        self._udp_socket.close()
        self._udp_socket = None

    def send(self, data: bytearray) -> int:
        """
        Send the data to the target drone

        :param data: message to send to the target drone
        :return: the number of bytes sent or -1 in case of the socket is closed
        """

        if not self._udp_socket is None:
            return self._udp_socket.sendto(data, (self._dst_ip, self._dst_port))
        else:
            return -1

    def receive(self) -> bytes:
        """
        Receive the data from the target drone
        """

        # TODO: valutare meccanismo di timeout
        data, _ = self._udp_socket.recvfrom(self._buffer_size)

        #TODO: analisi dati ricevuti
        #print(data)
        return data