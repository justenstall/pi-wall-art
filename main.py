import time
import sys

from src import spotify
from src.matrix import Matrix
from src import gradients

def main():
	m = Matrix()
	gradients.infinite_random_gradient(m)

	try:
		print("Press CTRL-C to stop.")
		while True:
			time.sleep(100)
	except KeyboardInterrupt:
		sys.exit(0)

if __name__ == "__main__":
	main()