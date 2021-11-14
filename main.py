import sys
import os
import argparse
import paramiko
from random import choice
from multiprocessing import Process
from Simulator import simulator


# PI_ADDRESSES = ["10.35.70.29", "10.35.70.20"]
PI_ADDRESSES = ["10.35.70.29"]
SSH_KEY = f"{os.environ['HOME']}/.ssh/id_rsa.pub"
USER = os.environ['USER']


def run_simulator(world_size: int, address: str, port: str):
    sim = simulator(
        size=world_size,
        host=address,
        port=port)
    sim()

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
        
        print(stderr.decode('utf-8'))
        print(stdout.decode('utf-8'))

def setup_ships(number):
    pass

def main():
    parser = argparse.ArgumentParser(
        description="Simulate some space mail!")
    parser.add_argument(
        '--size',
        type=int,
        default=1e5,
        help="The size of the simulated universe, default is 1e5 km")
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
        "--num-ships",
        type=int,
        default=10,
        help="Number of ships to spawn, default = 10")
    parser.add_argument(
        "--num-stations",
        type=int,
        default=1,
        help="Number of stations to spawn, default = 1")
    args = parser.parse_args()
    sim_proc = Process(target=run_simulator, args=(args.size, args.host, args.port))
    sim_proc.start()
    import ipdb; ipdb.set_trace()
    # sim_proc.join()

    setup_stations(args.num_stations, args.host, args.port)
    

if __name__ == "__main__":
    sys.exit(main())