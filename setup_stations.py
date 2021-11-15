import os
import paramiko
import argparse
import time
from random import choice
import select

# PI_ADDRESSES = ["10.35.70.29", "10.35.70.30"]
PI_ADDRESSES = ["127.0.0.1"]

SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']

def worker(stdout, stderr):
    # Wait for the command to terminate
    print(f"Status of worker is {stdout.channel.exit_status_ready()}")
    while not stdout.channel.exit_status_ready():
        time.sleep(1)
        print(f"Status of worker is {stdout.channel.exit_status_ready()}")
        if stdout.channel.recv_ready():
            # Only print data if there is data to read in the channel
            print(f"Worker stdout.channel.recv_ready: {stdout.channel.recv_ready()}")
            rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            if len(rl) > 0:
                # Print data from stdout
                print(f"Output: {stdout.channel.recv(1024).decode('utf-8')}")

def setup_stations(num_stations: int, server_address: str, port: str):
    print("Starting station setup")

    station_address = choice(PI_ADDRESSES)
    ssh_connections = {}
    workers = {}
    for _ in range(num_stations):
        # import ipdb; ipdb.set_trace()
        station_address = choice(PI_ADDRESSES)
        cmd = f'bash ~/projects/scalable_project_3/start_station.sh {server_address} {port} &'

        if not (new_client := ssh_connections.get(station_address)):
            print(f"starting new station on device {station_address}")
            new_client = paramiko.SSHClient()
            new_client.load_system_host_keys()
            new_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            new_client.connect(station_address, username=USER, key_filename=SSH_KEY)
            ssh_connections[station_address] = new_client
        else:
            print(f"Using previously established connection {station_address}")

        (_, stdout, stderr) = ssh_connections[station_address].exec_command(cmd)
        print("Reading output from master")


        workers[station_address] = worker(stdout, stderr)
        print("Finished reading output from master")


        # for line in stderr.readlines():
        #     print(line)
        # for line in stdout.readlines():
        #     print(line)

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
    args = parser.parse_args()
    setup_stations(
        num_stations=args.num_stations,
        server_address=args.host,
        port=args.port)

if __name__ == "__main__":
    main()