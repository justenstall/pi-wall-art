import ee
# from pprint import pprint

# import matrix

import folium

# Trigger the authentication flow.
ee.Authenticate(auth_mode="appdefault")

# Initialize the library.
ee.Initialize()

# Load a Landsat image.
# img = ee.Image('LANDSAT/LT05/C01/T1_SR/LT05_034033_20000913')

# # Print image object WITHOUT call to getInfo(); prints serialized request instructions.
# # print(img)

# # Print image object WITH call to getInfo(); prints image metadata.
# pprint(img.getInfo())

image_viz_params = {
    'bands': ['B5', 'B4', 'B3'],
    'min': 0,
    'max': 0.5,
    'gamma': [0.95, 1.1, 1]
}

# mat = matrix.init_matrix()

# Load an image.
image = ee.Image('LANDSAT/LC08/C02/T1_TOA/LC08_044034_20140318')

print(image.getThumbURL({'bands': 'QA_PIXEL', 'dimensions': '64x64'}))