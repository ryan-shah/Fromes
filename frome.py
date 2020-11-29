import cv2, numpy as np
from sklearn.cluster import KMeans
from os import listdir
from os.path import isfile, join

def visualize_colors(colors, height=50, length=300):
	rect = np.zeros((height, length, 3), dtype=np.uint8)
	start = 0
	percent = 1.0 / len(colors)
	for color in colors:
		print(color[0], "{:0.2f}%".format(percent * 100))
		end = start + (percent * length)
		cv2.rectangle(rect, (int(start), 0), (int(end), height), \
			color.astype("uint8").tolist()[0], -1)
		start = end
	return rect

colors = []
dirname = 'muppet-pics'
files = [join(dirname, f) for f in listdir(dirname) if isfile(join(dirname, f))]
files = sorted(files)

for f in files:
	print('Processing ' + f + '...')
	# Load image and convert to a list of pixels
	image = cv2.imread(f)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	reshape = image.reshape((image.shape[0] * image.shape[1], 3))

	# Find and display most dominant colors
	cluster = KMeans(n_clusters=1).fit(reshape)
	colors.append(cluster.cluster_centers_)

# 720
# visualize = visualize_colors(colors, 720, 1280)
# 1080
visualize = visualize_colors(colors, 1080, 1920)
visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
cv2.imshow('visualize', visualize)
cv2.waitKey()

