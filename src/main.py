"""
    This is the main command line interface, it initializes the
    ControllerManager and the EntityManager servers, and listens for 
    user generated global events.
"""
import sys
import argparse
import configparser
from simulator import Simulator

config = configparser.ConfigParser()
config.read('../Environment.ini')
config = config['config']

def main():
    parser = argparse.ArgumentParser(
        description="Simulate some space mail!")
    parser.add_argument(
        '--size',
        type=int,
        default=config['size'],
        help=f"The size of the simulated universe, default is {config['size']} km")
    parser.add_argument(
        "--host",
        type=str,
        default=config['hostIP'],
        help=f"The IP address to bind to, by default is set to {config['hostIP']}. If you want anyone else to see the server run with 0.0.0.0")
    parser.add_argument(
        "--port",
        type=int,
        default=config['port'],
        help=f"The port the simulator should run on, default is {config['port']}")
    parser.add_argument(
        "--num-ships",
        type=int,
        default=config['num_ships'],
        help=f"The number of ships to spawn, default is {config['num_ships']}")
    parser.add_argument(
        "--dont-setup",
        action="store_true",
        help="Dont setup the entity_manager and controller_manager servers, useful when debugging. Assumes the servers have already been setup manually, on the port [PORT + 1]")
    args = parser.parse_args()
    sim = Simulator(
        size=args.size,
        num_ships=args.num_ships,
        host=args.host,
        port=args.port,
        dont_setup=args.dont_setup)
    try:
        sim()
    except KeyboardInterrupt as e:
        print("Caught interrupt KeyboardInterrupt")
    except Exception as e:
        print(f"Caught exception {repr(e)}")
    finally:
        sim.shutdown_services()
        sim.shutdown()
    return 0


if __name__ == "__main__":
    sys.exit(main())