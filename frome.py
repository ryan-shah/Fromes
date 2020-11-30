#!/usr/bin/python

import cv2, numpy as np
from sklearn.cluster import KMeans
from os import listdir, makedirs
from os.path import isfile, join, exists
import sys, getopt

directory_name = 'frome_images'
in_file = ''
out_file = 'out.png'

resolutions = {}
resolutions['8k'] = (4320, 7680)
resolutions['4k'] = (3840, 2160)
resolutions['1080'] = (1920, 1080)
resolutions['720'] = (1280, 720)
resolutions['480'] = (852, 480)
resolutions['360'] = (640, 360)
resolutions['240'] = (320, 240)
resolution = resolutions['1080']


def main(argv):
	global directory_name
	global in_file
	global out_file
	global resolutions
	global resolution

	try:
		opts, args = getopt.getopt(argv, "d:hi:o:r:")
	except getopt.GetoptError:
		print('Error: check arguments - ', argv)
		print_help()
		exit(2)

	for opt, arg in opts:
		if opt == '-h':
			print_help()
			exit()
		elif opt == '-d':
			directory_name = arg
		elif opt == '-i':
			in_file = arg
		elif opt == '-r':
			if arg not in resolutions.keys():
				print('Error: invalid resolution - ' + arg)
				print_help()
				exit(2)
			resolution = resolutions[arg]
		elif opt == '-o':
			out_file = arg

	print(directory_name)
	print(in_file)
	print(resolution)
	print(out_file)
	generate_images()

def generate_images():
	if not exists(directory_name):
		makedirs(directory_name)
	cmd = 'ffmpeg -i ' + in_file + ' ' + join(directory_name, 'img%04d.png')
	print(cmd)
#	os.system('ffmpeg -i muppet.mp4 muppet-pics/img%04d.png')

def print_help():
	print('Create from video file')
	print('\tfrome.py -i <video-input> [-d <images-directory-name>]')
	print('Create from directory of images')
	print('\tfrome.py -d <images-directory-name>')
	print('Extra options:')
	r_sizes = '|'.join(resolutions.keys())
	print('\tResolution: -r [' + r_sizes + ']')
	print('\tOutput file: -o <filename>')



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

def process_images():
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
	cv2.imwrite('out.png', visualize)
	cv2.imshow('visualize', visualize)
	cv2.waitKey()


if __name__ == "__main__":
	if len(sys.argv) < 1:
		print('Error: invalid number of args')
		print_help()
		exit(2)
	main(sys.argv[1:])
