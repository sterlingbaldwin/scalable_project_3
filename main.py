import sys
import argparse
from MainController import Controller
import configparser

config = configparser.ConfigParser()
config.read('Environment.ini')

def main():
    parser = argparse.ArgumentParser(
        description="Simulate some space mail!")
    parser.add_argument(
        '--size',
        type=int,
        default=config['MainController']['size'],
        help=f"The size of the simulated universe, default is {config['MainController']['size']} km")
    parser.add_argument(
        "--host",
        type=str,
        default=config['MainController']['hostIP'],
        help=f"The IP address to bind to, by default is set to {config['MainController']['hostIP']}. If you want anyone else to see the server run with 0.0.0.0")
    parser.add_argument(
        "--port",
        type=str,
        default=config['MainController']['port'],
        help=f"The port the simulator should run on, default is {config['MainController']['port']}")
    parser.add_argument(
        "--num-ships",
        type=int,
        default=config['MainController']['num_ships'],
        help=f"The number of ships to spawn, default is {config['MainController']['num_ships']}")
    parser.add_argument(
        "--num-stations",
        type=int,
        default=config['MainController']['num_stations'],
        help=f"The number of stations to spawn, default is {config['MainController']['num_stations']}")
    args = parser.parse_args()
    controller = Controller(
        size=args.size,
        host=args.host,
        port=args.port)
    controller()


if __name__ == "__main__":
    sys.exit(main())