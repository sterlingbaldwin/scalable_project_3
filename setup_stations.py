import os
import paramiko
import argparse
from pathlib import Path
from random import choice
from uuid import uuid4

PI_ADDRESSES = ["10.35.70.29", "10.35.70.30"]
# PI_ADDRESSES = ["127.0.0.1"]

SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']

def setup_stations(num_stations: int, server_address: str, port: str, logdir: str):
    print("Starting station setup")

    for _ in range(num_stations):
        station_address = choice(PI_ADDRESSES)
        station_id = uuid4().hex

        cmd = f'python ~/projects/scalable_project_3/start_station.py {server_address} {port} {station_id} > {Path(logdir).absolute()}/{station_id}.out 2>&1'

        new_client = paramiko.SSHClient()
        new_client.load_system_host_keys()
        new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        new_client.connect(station_address, username=USER, key_filename=SSH_KEY)

        print(f"executing command: {cmd}")
        new_client.exec_command(cmd)
        print(f"Finished setting up station on {station_address}")

    return

def main():
    parser = argparse.ArgumentParser(
        description="Start the stations")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The IP address that the simulator is running on")
    parser.add_argument(
        "--port",
        type=str,
        default="5000",
        help="The port the simulator should run on, default is 5000")
    parser.add_argument(
        "--num-stations",
        type=int,
        default=1,
        help="Number of stations to spawn, default = 1")
    parser.add_argument(
        "--log",
        type=str,
        default="station_logs",
        help="directory of where to store the station output")
    args = parser.parse_args()
    if not os.path.exists(args.log):
        os.mkdir(args.log)
    setup_stations(
        num_stations=args.num_stations,
        server_address=args.host,
        port=args.port,
        logdir=args.log)

if __name__ == "__main__":
    main()