import time
import sys

from src import spotify
from src import matrix

def main():
	m = matrix.init_matrix()
	spotify.print_my_playlists(m)

	try:
		print("Press CTRL-C to stop.")
		while True:
			time.sleep(100)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == "__main__":
	main()