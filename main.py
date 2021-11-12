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
        '--stations',
        type=int,
        default=10,
        help="The number of fixed stations, default is 10")
    parser.add_argument(
        '--ships',
        type=int,
        default=100,
        help="The number of moving ships, default is 100")
    args = parser.parse_args()
    sim = simulator(
        num_ships=args.ships,
        num_stations=args.stations,
        size=args.size)

if __name__ == "__main__":
    sys.exit(main())