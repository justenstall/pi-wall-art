import time
import sys

from src import spotify
from src.matrix import Matrix

def main():
	m = Matrix()
	spotify.print_my_playlists(m)

	try:
		print("Press CTRL-C to stop.")
		while True:
			time.sleep(100)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == "__main__":
	main()