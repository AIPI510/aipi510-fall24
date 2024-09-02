import sys
from opensky_api import OpenSkyApi

def main(*argv):
    """
    Entry Point
    """
    api = OpenSkyApi()
    s = api.get_states()
    print(s)

if __name__ == "__main__":
    main(sys.argv)

