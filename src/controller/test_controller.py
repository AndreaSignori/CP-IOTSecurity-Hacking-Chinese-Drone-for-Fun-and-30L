import time

from src.controller.flycontroller import FlyController

if __name__ == '__main__':
    controller = FlyController(dst_ip='192.168.1.1', dst_port=7099, heartbeat_interval=1, heartbeat_msg=bytearray([1, 1]),buffer_size=1024)

    std_config = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x2, 0x99]) # standard position for the controller
    takeoff_cmd = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x1, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3, 0x99])
    land_cmd = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x1, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3, 0x99])
    forward_cmd = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x75, 0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0,0xf7, 0x99])

    """
    NOTE:
        * pause after every command is needed in order to give some time to the drone to actuate the command
        * the command is executed a several time in order to see some concrete action 
    """

    if controller.start():
        controller.send(std_config) # needed in order to establish a connection because enable the possibility to send commands to the drone

        for _ in range(15):
            controller.send(takeoff_cmd)
            time.sleep(0.5)

        time.sleep(2) # use to keep the drone in air

        for _ in range(10):
            controller.send(std_config)
            time.sleep(0.5)

        for _ in range(10):
            controller.send(forward_cmd)
            time.sleep(0.5)


        for _ in range(10):
            controller.send(land_cmd)
            time.sleep(0.5)

        controller.stop()