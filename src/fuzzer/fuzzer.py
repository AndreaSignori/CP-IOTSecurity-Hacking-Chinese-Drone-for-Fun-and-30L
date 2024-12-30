import time
import random

from src.controller.flycontroller import FlyController

def generate_rnd_command() -> bytearray:
    # Define every array elements that shoulld be fuzz
    controlByte1 = random.randint(0, 255)
    controlByte2 = random.randint(0, 255)
    controlAccelerator = random.randint(0, 255)
    controlTurn = random.randint(0, 255)
    i9 = random.randint(0, 15)
    i10 = random.randint(0, 15)
    XORControl = i9 ^ (((controlByte1 ^ controlByte2) ^ controlAccelerator) ^ controlTurn) ^ (i10 & 255)

    # Define the array with random values for specific indices
    bArr = [
        3,
        102,
        20,
        controlByte1,
        controlByte2,
        controlAccelerator,
        controlTurn,
        i9,
        i10,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
        XORControl,
        -103
    ]

    return bytearray([(value % 256) for value in bArr])

if __name__ == "__main__":
    MAX_ITERATIONS = 46500
    controller = FlyController(dst_ip='192.168.1.1', dst_port=7099, heartbeat_interval=1, heartbeat_msg=bytearray([1, 1]), buffer_size=20)

    #std_config = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x2, 0x99])
    takeoff_cmd = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x1, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3, 0x99])
    landing_cmd = bytearray([0x3, 0x66, 0x14, 0x80, 0x80, 0x80, 0x80, 0x1, 0x2, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3, 0x99])

    is_power_on = controller.start()
    fuzzer_log_path = "./fuzzer.log"
    iter_num = 0

    # drone take-off
    for _ in range(10):
        controller.send(takeoff_cmd)
        #time.sleep(0.5)

    # aggiungere upper bound per il numero di messaggi

    while is_power_on or iter_num < MAX_ITERATIONS:
        fuzz_command = generate_rnd_command()

        if not fuzz_command.hex() == takeoff_cmd.hex():
            try:
                controller.send(fuzz_command)
                time.sleep(0.1)

                drone_heartbeat = controller.receive(wait=0.2) # si può ridurre

                with open(fuzzer_log_path, "a") as f:
                    str = f"{fuzz_command.hex()}\t"

                    if drone_heartbeat is None:
                        is_power_on = False # then end the fuzzer execution because we suppose that the drone is unreachable
                        str += "FAILED\n"
                    else:
                        str += "OK\n"

                    f.write(str)

                iter_num += 1
            except OSError:
                print("Drone is unreachable!")
                break

    # drone landing
    for _ in range(10):
        controller.send(landing_cmd)
        #time.sleep(0.5)

    controller.stop()