from PIL import Image, ImageOps

class MatrixImage:
	def __init__(self, im: Image.Image, url: str, description: str) -> None:
		self.image = im
		self.url = url
		self.description = description
