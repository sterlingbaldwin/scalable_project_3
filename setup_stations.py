import os
import paramiko
import argparse
from random import choice

# PI_ADDRESSES = ["10.35.70.29", "10.35.70.20"]
PI_ADDRESSES = ["10.35.70.29"]
SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']

def setup_stations(num_stations: int, address: str, port: str):
    print("Starting station setup")
    for _ in range(num_stations):
        address = choice(PI_ADDRESSES)
        print(f"starting new station on {address}")
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(address, username=USER, key_filename=SSH_KEY)
        cmd = f'bash ~/projects/scalable_project_3/start_station.sh {address} {port}'
        (_, stdout, stderr) = client.exec_command(cmd)
        
        for line in stderr.readlines():
            print(line)
        for line in stdout.readlines():
            print(line)

def main():
    parser = argparse.ArgumentParser(
        description="Start the stations")
    parser.add_argument(
        "--host",
        type=str,
        default="127.0.0.1",
        help="The IP address to bind to, by default is set to 172.0.0.1. If you want anyone else to see the server run with 0.0.0.0")
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
    args = parser.parse_args()
    setup_stations(
        num_stations=args.num_stations,
        address=args.host,
        port=args.port)

if __name__ == "__main__":
    main()