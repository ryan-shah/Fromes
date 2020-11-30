#!/usr/bin/python
from __future__ import print_function
import cv2, numpy as np
from sklearn.cluster import KMeans
from os import listdir, makedirs, system
from os.path import isfile, join, exists, basename
import sys, getopt
import threading

# file management
directory_name = 'frome_images'
in_file = ''
out_file = 'out.png'

# output resolutions
resolutions = {}
resolution = (300, 50)

# num threads
threads = 1

# list of colors (RGB, ID)
colors = []

# counts # of processed images per thread
counts = [0]

# number of frames per second to capture from the video
rate = 0

# set the available resolutions
def setup_resolutions():
	global resolutions
	resolutions['8000'] = (7680, 4320)
	resolutions['4000'] = (3840, 2160)
	resolutions['1080'] = (1920, 1080)
	resolutions['720'] = (1280, 720)
	resolutions['480'] = (852, 480)
	resolutions['360'] = (640, 360)
	resolutions['240'] = (320, 240)

# main function
def main(argv):
	global directory_name
	global in_file
	global out_file
	global resolutions
	global resolution
	global threads
	global counts
	global rate
	setup_resolutions()

	# define command-line parameters
	try:
		opts, args = getopt.getopt(argv, "d:hi:o:q:r:t:")
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
		elif opt == '-q':
			if arg not in resolutions.keys():
				print('Error: invalid resolution - ' + arg)
				print_help()
				exit(2)
			resolution = resolutions[arg]
		elif opt == '-o':
			out_file = arg
		elif opt == '-t':
			threads = int(arg)
			counts = [0] * threads
		elif opt == '-r':
			rate = int(arg)

	# create image directory if it doesn't exist
	if not exists(directory_name):
		makedirs(directory_name)

	# if in_file exists, create images from video
	if not in_file == '':
		print("Generating images from " + in_file + " in " + directory_name + "...")
		generate_images()

	# get list of files
	files = [join(directory_name, f) for f in listdir(directory_name) if isfile(join(directory_name, f))]
	# put in order
	files = sorted(files)
	# split per thread
	split_files = np.array_split(files, threads)
	# keep track of threads
	ids = []
	# generate threads
	for index in range(threads):
		x = threading.Thread(target=process_images, args=(split_files[index], index,))
		ids.append(x)
		x.start()

	# Report thread progress
	while sum(counts) < len(files):
		percent = (1.0 + sum(counts))/len(files)
		print("\rProcessing Images with " + str(threads) + " threads: " + \
			str(round(percent * 100, 2)) + "%", end='')

	# Join threads back together
	for x in ids:
		x.join()
	print("\rProcessing Done! Outputing to " + out_file + "...")

	# Show & Save final result
	generate_result()

# ffmpeg command line
def generate_images():
	global rate
	rate_opt = ' '
	if not rate == 0:
		rate_opt = ' -r ' + str(rate) + ' '
	cmd = 'ffmpeg -i ' + in_file + rate_opt + join(directory_name, 'img%04d.jpeg')
	print(cmd)
	result = system(cmd)
	if not result == 0:
		print('ffmpeg returned with exit code ' + str(result))
		exit(1)

# prints help info
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
	print('\tResolution Quality: -q [' + r_sizes + ']')
	print('\tOutput file: -o <filename>')
	print('\tThread count: -t <num_threads>')
	print('\tFrames Per Second: -r <frame-rate>')

# creates the final image
def visualize_colors(colors, height=50, length=300):
	rect = np.zeros((height, length, 3), dtype=np.uint8)
	start = 0
	percent = 1.0 / len(colors)
	for color in colors:
		end = start + (percent * length)
		cv2.rectangle(rect, (int(start), 0), (int(end), height), \
			color[0].astype("uint8").tolist()[0], -1)
		start = end
	return rect

# gets the id of the file name to ensure the colors are in order
def get_id(file):
	return int(basename(file)[3:-5])

# gets the most common colors in a list of images
def process_images(files, index):
	global colors
	global directory_name
	global resolution
	global counts

	for f in files:
		# Load image and convert to a list of pixels
		image = cv2.imread(f)
		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		reshape = image.reshape((image.shape[0] * image.shape[1], 3))

		# Find and display most dominant colors
		cluster = KMeans(n_clusters=1).fit(reshape)
		id = get_id(f)
		colors.append((cluster.cluster_centers_, id))
		counts[index] += 1

# creates the result and outputs it
def generate_result():
	colors.sort(key = lambda x: x[1])
	visualize = visualize_colors(colors, resolution[1], resolution[0])
	visualize = cv2.cvtColor(visualize, cv2.COLOR_RGB2BGR)
	cv2.imwrite(out_file, visualize)
	cv2.imshow(out_file, visualize)
	cv2.waitKey()

if __name__ == "__main__":
	if len(sys.argv) < 2:
		print('Error: invalid number of args')
		print_help()
		exit(2)
	main(sys.argv[1:])
