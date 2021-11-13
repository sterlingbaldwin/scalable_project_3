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
    args = parser.parse_args()
    sim = simulator(
        size=args.size,
        host=args.host)
    sim()

if __name__ == "__main__":
    sys.exit(main())