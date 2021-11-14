import sys
import argparse
from multiprocessing import Process
from Simulator import simulator

def run_simulator(world_size: int, address: str):
    sim = simulator(
        size=world_size,
        host=address)
    sim()

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
    args = parser.parse_args()
    sim_proc = Process(target=run_simulator, args=(args.size, args.host))
    sim_proc.start()
    sim_proc.join()
    

if __name__ == "__main__":
    sys.exit(main())