from rgbmatrix import RGBMatrix, RGBMatrixOptions

def init_matrix():
	# Initialize RGB Matrix object
	matrix_options = RGBMatrixOptions()
	matrix_options.rows = 64
	matrix_options.cols = 64
	# matrix_options.show_refresh_rate = True
	matrix_options.brightness = 60
	matrix_options.pwm_dither_bits = 1
	matrix_options.chain_length = 1
	matrix_options.parallel = 1
	matrix_options.hardware_mapping = "adafruit-hat-pwm"
	matrix_options.limit_refresh_rate_hz = 120

	matrix = RGBMatrix(options=matrix_options)

	return matrix
