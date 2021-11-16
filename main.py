import sys
import argparse
from Simulator import simulator

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
    sim = simulator(
        size=args.size,
        host=args.host,
        port=args.port)
    sim()
    

if __name__ == "__main__":
    sys.exit(main())