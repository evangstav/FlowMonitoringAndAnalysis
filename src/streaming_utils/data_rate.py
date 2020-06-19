import subprocess
import time
import argparse


class DataRate:
    def __init__(self, interface="lo", duration=1):
        self.interface = interface
        self.duration = duration

    def get_rx_bytes(self):
        output = subprocess.check_output(
            "ip -s link show dev %s" % self.interface,
            stderr=subprocess.STDOUT,
            shell=True,
        )
        output_array = output.decode("utf-8").split("\n")
        rx_bytes = int(output_array[3].split()[0])
        return rx_bytes

    def get_data_rate(self):
        bytes_1 = self.get_rx_bytes()
        time.sleep(self.duration)
        bytes_2 = self.get_rx_bytes()
        rx_rate = round((bytes_2 - bytes_1) / (self.duration * 1024.0 * 1024.0), 4)
        return rx_rate


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--interface", default="lo")
    args = parser.parse_args()
    data_rate = DataRate(interface=args.interface)
    while True:
        rate = data_rate.get_data_rate()
        print("Throughput: " + str(rate) + " Mbps.")
