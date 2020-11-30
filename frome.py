#!/usr/bin/python

import cv2, numpy as np
from sklearn.cluster import KMeans
from os import listdir, makedirs, system
from os.path import isfile, join, exists
import sys, getopt
from copy import deepcopy
import concurrent.futures

directory_name = 'frome_images'
in_file = ''
out_file = 'out.png'

resolutions = {}
resolution = (300, 50)

threads = 1

colors = []

def setup_resolutions():
	global resolutions
	resolutions['8000'] = (7680, 4320)
	resolutions['4000'] = (3840, 2160)
	resolutions['1080'] = (1920, 1080)
	resolutions['720'] = (1280, 720)
	resolutions['480'] = (852, 480)
	resolutions['360'] = (640, 360)
	resolutions['240'] = (320, 240)


def main(argv):
	global directory_name
	global in_file
	global out_file
	global resolutions
	global resolution
	global threads
	setup_resolutions()

	try:
		opts, args = getopt.getopt(argv, "d:hi:o:r:t:")
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
		elif opt == '-t':
			threads = int(arg)

	if not in_file == '':
		generate_images()
	files = [join(directory_name, f) for f in listdir(directory_name) if isfile(join(directory_name, f))]
	files = sorted(files)
	split_files = np.array_split(files, threads)
	with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
	        executor.map(process_images, split_files)
	generate_result()

def generate_images():
	if not exists(directory_name):
		makedirs(directory_name)
	cmd = 'ffmpeg -i ' + in_file + ' ' + join(directory_name, 'img%04d.png')
	print(cmd)
	system(cmd)

def print_help():
	global resolutions
	print('Create from video file')
	print('\tfrome.py -i <video-input> [-d <images-directory-name>]')
	print('Create from directory of images')
	print('\tfrome.py -d <images-directory-name>')
	print('Extra options:')
	r_values = resolutions.keys()
	r_values.sort(reverse=True, key=int)
	r_sizes = '|'.join(r_values)
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
			color[0].astype("uint8").tolist()[0], -1)
		start = end
	return rect

def get_id(file):
	start = file.find('img')
	return int(file[start+3:-4])

def process_images(files):
	global colors
	global directory_name
	global resolution

	for f in files:
		print('Processing ' + f + '...')
		# Load image and convert to a list of pixels
		image = cv2.imread(f)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		reshape = image.reshape((image.shape[0] * image.shape[1], 3))

		# Find and display most dominant colors
		cluster = KMeans(n_clusters=1).fit(reshape)
		id = get_id(f)
		colors.append((cluster.cluster_centers_, id))

def generate_result():
	colors.sort(key = lambda x: x[1])
	visualize = visualize_colors(colors, resolution[1], resolution[0])
	visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
	cv2.imwrite(out_file, visualize)
	cv2.imshow(out_file, visualize)
	cv2.waitKey()

if __name__ == "__main__":
	if len(sys.argv) < 1:
		print('Error: invalid number of args')
		print_help()
		exit(2)
	main(sys.argv[1:])
